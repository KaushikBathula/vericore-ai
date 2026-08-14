import RequirementForm from "@/components/forms/RequirementForm";
export default function RequirementPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">
          Requirement Input
        </h1>

        <p className="text-muted-foreground mt-2">
          Describe the hardware design you want VeriCore AI to generate.
        </p>
      </div>
      <RequirementForm />
    </div>
  );
}