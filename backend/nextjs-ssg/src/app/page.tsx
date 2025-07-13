import { readFileSync } from "fs";
import { join } from "path";
import { ComponentRenderer } from "@shared/index";
import { PageData } from "@/types";

async function getPageData(): Promise<PageData> {
  try {
    const dataPath = join(process.cwd(), "data", "page.json");
    const data = readFileSync(dataPath, "utf8");
    return JSON.parse(data);
  } catch {
    // Fallback data for development
    return {
      id: 1,
      title: "Landing Page",
      description: "Generated landing page",
      slug: "home",
      subdomain: "demo",
      config: { theme: "default" },
      components: [],
    };
  }
}

export default async function Home() {
  const pageData = await getPageData();

  return (
    <main>
      <ComponentRenderer pageData={pageData} />
    </main>
  );
}
