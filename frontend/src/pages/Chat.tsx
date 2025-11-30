import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Send, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import chambiImage from "@/assets/chambi-capybara.svg";
import { AuthForm } from "@/components/AuthForm";

const Chat = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [message, setMessage] = useState("");
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleLogin = (t: string, u: string) => {
    setToken(t);
    setUsername(u);
  };

  const fetchPictograms = async (text: string) => {
    try {
      const response = await fetch("http://127.0.0.1:8001/recommend/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ selected: text.split(" ") }),
      });

      if (!response.ok) throw new Error("Failed to fetch pictograms");

      const data = await response.json();
      setRecommendations(data.pictograms);

      toast({
        title: "¡Muy bien! 🌟",
        description: "Aquí tienes los pictogramas para tu frase.",
      });
    } catch (error) {
      console.error(error);
      toast({
        title: "Error 😢",
        description: "No pude conectar con el profesor Chambi.",
        variant: "destructive",
      });
    }
  };

  const handleSendMessage = async () => {
    if (message.trim()) {
      setLoading(true);
      await fetchPictograms(message);
      setLoading(false);
      setMessage("");
    }
  };

  const handleImageUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Predict image class using Backend
      const response = await fetch("http://127.0.0.1:8001/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to predict image");

      const data = await response.json();
      const className = data.class_name;

      toast({
        title: "¡Imagen analizada! 📸",
        description: `Parece que es: ${className}. Vamos a ver cómo se dice en pictogramas.`,
      });

      // Get pictograms for the predicted class
      await fetchPictograms(className);
    } catch (error) {
      console.error(error);
      toast({
        title: "Error 😢",
        description: "No pude analizar la imagen.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
      // Reset file input
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-background p-4 relative overflow-hidden">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-32 right-20 w-40 h-40 bg-primary/30 rounded-full animate-float blur-3xl" />
          <div className="absolute bottom-32 left-20 w-48 h-48 bg-secondary/30 rounded-full animate-bounce-slow blur-3xl" />
        </div>
        <Button
          variant="ghost"
          onClick={() => navigate("/")}
          className="absolute top-4 left-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" /> Volver
        </Button>
        <div className="z-10 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold gradient-primary bg-clip-text text-transparent mb-2">
              Aprende con Chambi
            </h1>
            <p className="text-muted-foreground">
              Inicia sesión para comenzar tu clase.
            </p>
          </div>
          <AuthForm onLogin={handleLogin} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-background relative overflow-hidden">
      {/* Animated background shapes */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-32 right-20 w-40 h-40 bg-primary/30 rounded-full animate-float blur-3xl" />
        <div className="absolute bottom-32 left-20 w-48 h-48 bg-secondary/30 rounded-full animate-bounce-slow blur-3xl" />
        <div className="absolute top-1/2 right-1/3 w-36 h-36 bg-accent/30 rounded-full animate-pulse-slow blur-3xl" />
      </div>

      {/* Header */}
      <header className="border-b border-border/40 bg-card/80 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/")}
            className="hover:bg-primary/10"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Salir
          </Button>
          <h1 className="text-xl font-bold gradient-primary bg-clip-text text-transparent md:text-2xl">
            Aprende con Chambi
          </h1>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium hidden md:inline-block">
              Hola, {username}
            </span>
            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
              {username?.[0].toUpperCase()}
            </div>
          </div>
        </div>
      </header>

      {/* Chat area */}
      <main className="flex-1 container mx-auto px-4 py-8 max-w-4xl relative z-10 flex flex-col gap-6">
        {/* Welcome message with Chambi */}
        <div className="flex flex-col items-center gap-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
          {/* Chambi the Capybara */}
          <div className="relative group">
            <div className="absolute -inset-4 bg-primary/20 rounded-full blur-xl animate-pulse-slow group-hover:bg-primary/30 transition-colors" />
            <img
              src={chambiImage}
              alt="Chambi el Capibara"
              className="w-32 h-32 md:w-40 md:h-40 relative z-10 animate-bounce-slow"
            />
          </div>

          {/* Speech bubble */}
          <Card className="max-w-xl p-6 bg-card/80 backdrop-blur-sm border-primary/20 shadow-lg text-center relative hover-lift">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-4 h-4 bg-card border-t border-l border-primary/20 transform rotate-45" />

            <p className="text-xl font-bold text-foreground mb-2">
              ¡Hola {username}! Soy el Profesor Chambi 🎓
            </p>
            <p className="text-muted-foreground">
              Escribe una frase o sube una foto, y te enseñaré los pictogramas.
            </p>
          </Card>
        </div>

        {/* Recommendations Area */}
        {recommendations.length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 animate-in zoom-in duration-500">
            {recommendations.map((picto) => (
              <Card
                key={picto.id}
                className="p-4 flex flex-col items-center hover-lift border-primary/10 bg-card/50 backdrop-blur-sm transition-all hover:bg-card"
              >
                <img
                  src={picto.url}
                  alt={picto.palabra}
                  className="w-full h-auto rounded-md mb-3 object-contain aspect-square"
                />
                <p className="text-lg font-bold text-center capitalize text-foreground">
                  {picto.palabra}
                </p>
              </Card>
            ))}
          </div>
        )}
      </main>

      {/* Input area */}
      <div className="sticky bottom-0 p-4 bg-background/80 backdrop-blur-lg border-t border-border/40 z-50">
        <div className="container max-w-4xl mx-auto flex gap-3 items-end">
          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            accept="image/*"
            onChange={handleFileChange}
          />
          <Button
            size="icon"
            variant="outline"
            onClick={handleImageUploadClick}
            className="h-12 w-12 rounded-xl border-2 hover:border-primary hover:text-primary transition-colors shrink-0"
          >
            <Upload className="w-5 h-5" />
          </Button>

          <div className="flex-1 relative">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              placeholder="Escribe aquí tu frase..."
              className="h-12 text-lg rounded-xl border-2 focus-visible:ring-primary/50 bg-background/50"
              disabled={loading}
            />
          </div>

          <Button
            size="icon"
            onClick={handleSendMessage}
            disabled={!message.trim() || loading}
            className="h-12 w-12 rounded-xl bg-primary hover:bg-primary/90 shadow-lg shadow-primary/25 shrink-0"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>
  );
};
export default Chat;
