interface CodeViewerProps {
  code: string | null;
  emptyMessage: string;
}

export default function CodeViewer({
  code,
  emptyMessage,
}: CodeViewerProps) {
  if (!code) {
    return (
      <div className="rounded-lg border bg-muted/30 p-4 text-sm text-muted-foreground">
        {emptyMessage}
      </div>
    );
  }

  const lines = code.replace(/\s+$/u, "").split("\n");

  return (
    <div className="max-h-[68vh] overflow-auto rounded-lg border bg-zinc-950 text-zinc-100">
      <table className="w-full border-collapse text-sm">
        <tbody>
          {lines.map((line, index) => (
            <tr key={`${index}-${line}`}>
              <td className="select-none border-r border-zinc-800 px-3 py-0.5 text-right font-mono text-xs text-zinc-500">
                {index + 1}
              </td>
              <td className="whitespace-pre px-4 py-0.5 font-mono">
                {line || " "}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
