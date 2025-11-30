import { useState, useEffect, useRef } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ChatRoomProps {
  username: string;
  roomId: string;
}

export const ChatRoom = ({ username, roomId }: ChatRoomProps) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(`ws://127.0.0.1:8001/chat/ws/${roomId}/${username}`);
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
    };

    return () => {
      ws.current?.close();
    };
  }, [roomId, username]);

  const sendMessage = async () => {
    if (input.trim() && ws.current) {
      // 1. Fetch pictograms first
      try {
        const response = await fetch("http://127.0.0.1:8001/recommend/convert", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ selected: input.split(" ") }),
        });
        const data = await response.json();
        const pictograms = data.pictograms;

        // 2. Send pictograms as content (serialized)
        // If no pictograms found, send text as fallback (or handle as you wish)
        const contentToSend = pictograms.length > 0 ? JSON.stringify(pictograms) : input;
        
        ws.current.send(JSON.stringify({ content: contentToSend, type: "message" }));
        setInput("");
      } catch (error) {
        console.error("Error fetching pictograms:", error);
        // Fallback to sending raw text if error
        ws.current.send(JSON.stringify({ content: input, type: "message" }));
        setInput("");
      }
    }
  };

  const renderMessageContent = (content: string) => {
    try {
      const pictos = JSON.parse(content);
      if (Array.isArray(pictos) && pictos.length > 0 && pictos[0].url) {
        return (
          <div className="flex flex-wrap gap-2">
            {pictos.map((p: any, i: number) => (
              <div key={i} className="flex flex-col items-center">
                <img src={p.url} alt={p.palabra} className="w-16 h-16 bg-white rounded-md" />
                <span className="text-[10px] font-bold capitalize mt-1">{p.palabra}</span>
              </div>
            ))}
          </div>
        );
      }
    } catch (e) {
      // Not JSON or not pictograms, render as text
    }
    return <p>{content}</p>;
  };

  return (
    <Card className="h-[600px] flex flex-col p-4 bg-card/95 backdrop-blur-sm border-2 border-border shadow-xl">
      <div className="mb-4 border-b pb-2 flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold gradient-primary bg-clip-text text-transparent">Sala: {roomId}</h2>
          <p className="text-sm text-muted-foreground">Usuario: {username}</p>
        </div>
        <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" title="Conectado" />
      </div>
      
      <div className="flex-1 pr-4 overflow-y-auto custom-scrollbar">
        <div className="space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.user === username ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${
                msg.type === "system" ? "bg-muted text-center w-full text-xs rounded-lg py-2" :
                msg.user === username ? "bg-primary text-primary-foreground rounded-tr-none" : "bg-secondary text-secondary-foreground rounded-tl-none"
              }`}>
                {msg.type !== "system" && <p className="text-xs font-bold mb-2 opacity-80">{msg.user}</p>}
                {renderMessageContent(msg.content)}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-4 flex gap-2">
        <Input 
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Escribe un mensaje para convertir a pictogramas..."
          className="rounded-xl border-2 focus-visible:ring-primary/50"
        />
        <Button onClick={sendMessage} className="rounded-xl px-6">Enviar</Button>
      </div>
    </Card>
  );
};
