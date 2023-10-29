import React from 'react';
import { createRoot } from "react-dom/client";

import { ErrorBoundary } from "react-error-boundary";
import { BrowserRouter } from "react-router-dom";

import { Provider as StoreProvider } from "react-redux"
import loadableVisibility from "react-loadable-visibility/loadable-components";
import pMinDelay from "p-min-delay"
import { timeout } from "promise-timeout"

import store from '@/store';
import PageLoadingAnimation from "@/components/Loading";

function FallbackComponent({ error, resetErrorBoundary }) {
  const [showDetail, setShowDetail] = useState(false);
  return (
    <div role="alert">
      <h3>Something went wrong on the client side.</h3>
      <>
        <i style={{ color: "red" }}>Error Message: {JSON.stringify(error.message)}</i>
        <br />
        <button onClick={() => setShowDetail(!showDetail)}>{showDetail ? "Hide" : "Show"}  Detail</button>
        <br />
        {/* to reset the error boundary and retry the render. */}
        <button onClick={() => resetErrorBoundary()}> Refresh</button>
        <br />
        <i hidden={!showDetail}>{error.stack}</i>
      </>
    </div>
  );
}

const logError = (error, info) => {
  // Do something with the error, e.g. log to an external API
  console.log(`Error boundary : ${error}`)
};

const LoadedApp = loadableVisibility(
  () => timeout(pMinDelay(import("@/App"), 1000), 10000), {
  fallback: <PageLoadingAnimation infoMessage="Loading Internal Application..." />
});

const main = () => {
  const root = createRoot(document.getElementById("root"));

  root.render(
    <StoreProvider store={store}>
      {/* <Sentry.ErrorBoundary fallback={<p>An error has occurred</p>}> */}
      <ErrorBoundary
        FallbackComponent={FallbackComponent}
        onReset={(details) => {
        }}
        onError={logError}
      >
        <BrowserRouter>
          <LoadedApp />
        </BrowserRouter>
      </ErrorBoundary>
      {/* </Sentry.ErrorBoundary> */}
    </StoreProvider>
  )
}

main();
