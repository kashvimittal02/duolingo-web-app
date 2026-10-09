"use client";

import { useEffect } from "react";
import { useRouter, useParams } from "next/navigation";

export default function SectionRedirectPage() {
  const router = useRouter();
  const params = useParams();

  useEffect(() => {
    const sectionId = params?.id ? String(params.id) : "1";
    router.replace(`/sections?unit=${sectionId}`);
  }, [router, params]);

  return (
    <div className="min-h-screen bg-white dark:bg-[#131f24] flex items-center justify-center">
      <div className="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
