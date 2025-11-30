import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

interface AuthFormProps {
  onLogin: (token: string, username: string) => void;
}

export const AuthForm = ({ onLogin }: AuthFormProps) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const endpoint = isLogin ? "http://127.0.0.1:8001/auth/token" : "http://127.0.0.1:8001/auth/register";
    
    try {
      let body;
      let headers = {};

      if (isLogin) {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);
        body = formData;
      } else {
        body = JSON.stringify({ username, password });
        headers = { "Content-Type": "application/json" };
      }

      const response = await fetch(endpoint, {
        method: "POST",
        headers: headers,
        body: body,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Auth failed");
      }

      const data = await response.json();
      
      if (isLogin) {
        onLogin(data.access_token, username);
        toast({ title: "¡Bienvenido! 👋" });
      } else {
        toast({ title: "Registro exitoso", description: "Ahora puedes iniciar sesión" });
        setIsLogin(true);
      }
    } catch (error: any) {
      toast({ title: "Error", description: error.message || "Credenciales inválidas", variant: "destructive" });
    }
  };

  const handleGuestLogin = () => {
    if (!username.trim()) {
      toast({ title: "Error", description: "Ingresa un nombre de usuario para entrar como invitado", variant: "destructive" });
      return;
    }
    // Generate a fake token for guest
    onLogin("guest-token", username + " (Invitado)");
    toast({ title: "¡Bienvenido Invitado! 👋" });
  };

  return (
    <Card className="p-6 w-full max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4 text-center">{isLogin ? "Iniciar Sesión" : "Registrarse"}</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input 
          placeholder="Usuario" 
          value={username} 
          onChange={e => setUsername(e.target.value)} 
        />
        <Input 
          type="password" 
          placeholder="Contraseña" 
          value={password} 
          onChange={e => setPassword(e.target.value)} 
        />
        <Button type="submit" className="w-full">
          {isLogin ? "Entrar" : "Registrarse"}
        </Button>
      </form>
      
      <div className="relative my-4">
        {/* Divider removed */}
      </div>

      {/* Guest login button removed */}

      <Button variant="link" onClick={() => setIsLogin(!isLogin)} className="w-full mt-2">
        {isLogin ? "¿No tienes cuenta? Regístrate" : "¿Ya tienes cuenta? Inicia sesión"}
      </Button>
    </Card>
  );
};
