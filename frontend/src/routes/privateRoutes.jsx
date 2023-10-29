import loadableVisibility from "react-loadable-visibility/loadable-components";
import pMinDelay from "p-min-delay"
import { timeout } from "promise-timeout"

import { ErrorBoundary } from "@/components/Error";
import { TooSmallLoadingComponent } from "@/components/Loading";

const LoadedIndexPage = loadableVisibility(
  () => timeout(pMinDelay(import("@/pages/IndexPage"), 1000), 10000), {
  fallback: <TooSmallLoadingComponent infoMessage="Loading index page..." />
});


const APP_VERSION = "app"

const privateRoutes = [
  {
    path: `/${APP_VERSION}`,
    errorElement: <ErrorBoundary />,
    children: [
      { index: true, element: <LoadedIndexPage /> },
      { path: "*", element: <>404!</> },
    ],
  },
]

export default privateRoutes;