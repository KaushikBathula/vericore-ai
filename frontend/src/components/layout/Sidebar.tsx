import Link from "next/link";
import {
  BookOpen,
  ClipboardList,
  FileCode,
  Gauge,
  Home,
  PlayCircle,
  Settings,
  TestTube,
} from "lucide-react";

const navigationItems = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: Home,
  },
  {
    label: "Requirements",
    href: "/requirements",
    icon: ClipboardList,
  },
  {
    label: "Pipeline",
    href: "/pipeline",
    icon: Gauge,
  },
  {
    label: "RTL Viewer",
    href: "/rtl",
    icon: FileCode,
  },
  {
    label: "Testbench",
    href: "/testbench",
    icon: TestTube,
  },
  {
    label: "Simulation",
    href: "/simulation",
    icon: PlayCircle,
  },
  {
    label: "Synthesis",
    href: "/synthesis",
    icon: Settings,
  },
  {
    label: "Documentation",
    href: "/documentation",
    icon: BookOpen,
  },
];

export default function Sidebar() {
  return (
    <aside className="flex w-64 flex-col border-r bg-muted/30">
      {/* Brand */}
      <div className="border-b p-6">
        <h1 className="text-xl font-bold tracking-tight">
          VeriCore AI
        </h1>

        <p className="mt-1 text-sm text-muted-foreground">
          RTL Design & Verification
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;

            return (
              <li key={item.label}>
                <Link
                  href={item.href}
                  className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-muted"
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}