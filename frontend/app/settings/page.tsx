import {Fa500Px, FaAccusoft, FaFile, FaGift, FaChartArea, FaAngleRight, FaArchive, FaHandsHelping, FaTable} from "react-icons/fa";
export default function SettingsPage() {
    return (
        <div>
            <h1 className="text-center font-bold text-2xl">Página de Configuración</h1>
            <p className="text-center">Aquí puedes ajustar las preferencias de tu restaurante.</p>
            <div className="mt-10">
                <h2 className="text-center">Checate los iconos tmb</h2>
                <div className="grid grid-cols-3 gap-4 mt-6">
                    <Fa500Px size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaAccusoft size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaFile size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaGift size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaChartArea size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaAngleRight size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaArchive size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaHandsHelping size={100} className="mx-auto mt-6 text-muted-foreground" />
                    <FaTable size={100} className="mx-auto mt-6 text-muted-foreground" />
                </div>
                
                <p className="text-center text-2xl mt-10">lo saque de aqui</p>
                <p className="text-center">https://react-icons.github.io/react-icons/icons?name=fa</p>

            </div>
        </div>
    );
}
