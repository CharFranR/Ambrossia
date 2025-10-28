import Image from "next/image";

export default function Home() {
  return (
    <div>
      <h1 className="text-center font-bold text-2xl">Papi esta es la pagina principal</h1>

      <p className="text-center">Chavis</p>
      <div className="flex justify-center mt-6">
        <Image
          src="/example.png"
          alt="Ambrossia Logo"
          width={300}
          height={300}
        />
        </div>
    </div>
      
  );
}
