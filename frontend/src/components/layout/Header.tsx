export default function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-background px-6">
      <div>
        <h2 className="text-xl font-semibold">
          Dashboard
        </h2>

        <p className="text-sm text-muted-foreground">
          Welcome to VeriCore AI
        </p>
      </div>

      <div className="rounded-full border px-3 py-1 text-sm font-medium">
        Ready
      </div>
    </header>
  );
}