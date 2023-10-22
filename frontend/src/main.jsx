import React from 'react';
import { createRoot } from "react-dom/client";

import LoadedApp from "@/App";

const main = () => {
  const root = createRoot(document.getElementById("root"));

  root.render(
    <React.StrictMode>
      <LoadedApp />
    </React.StrictMode>
  )
}

main();
