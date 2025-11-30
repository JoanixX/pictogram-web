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

  const sendMessage = () => {
    if (input.trim() && ws.current) {
      ws.current.send(JSON.stringify({ content: input, type: "message" }));
      setInput("");
    }
  };

  return (
    <Card className="h-[600px] flex flex-col p-4">
      <div className="mb-4 border-b pb-2">
        <h2 className="text-xl font-bold">Sala: {roomId}</h2>
        <p className="text-sm text-muted-foreground">Usuario: {username}</p>
      </div>
      
      <div className="flex-1 pr-4 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.user === username ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] rounded-lg p-3 ${
                msg.type === "system" ? "bg-muted text-center w-full text-xs" :
                msg.user === username ? "bg-primary text-primary-foreground" : "bg-secondary"
              }`}>
                {msg.type !== "system" && <p className="text-xs font-bold mb-1">{msg.user}</p>}
                <p>{msg.content}</p>
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
          placeholder="Escribe un mensaje..."
        />
        <Button onClick={sendMessage}>Enviar</Button>
      </div>
    </Card>
  );
};
