import { ChatInterface } from "@/components/ChatInterface";
import { Navbar } from "@/components/Navbar";

export default function Home() {
  return (
    <div className="flex flex-col h-screen bg-background">
      <Navbar />
      <main className="flex-1 overflow-hidden">
        <ChatInterface />
      </main>
    </div>
  );
}
