import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@radix-ui/react-dropdown-menu";

interface AreaDropdownProps {
  area: string;
  setArea: (value: string) => void;
  onAction?: () => void;
}

const AreaDropdown: React.FC<AreaDropdownProps> = ({ area, setArea, onAction }) => {
  const areas = ["1", "2", "3", "4", "5"];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="lg" onClick={onAction}>
          Área: {area}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        {areas.map((a, idx) => (
          <div key={a}>
            <DropdownMenuLabel>
              <Button variant="item" size="lg" onClick={() => setArea(a)}>
                Área: {a}
              </Button>
            </DropdownMenuLabel>
            {idx < areas.length - 1 && <DropdownMenuSeparator />}
          </div>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default AreaDropdown;