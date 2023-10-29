import { useState } from "react";
import Lottie from "lottie-react";
import ErrorAnimationData from "@/assets/error.json";
import {
  useRouteError,
  isRouteErrorResponse
} from "react-router-dom";

export const ErrorBoundaryComponent = ({ errorMessage = "", errorStack = "" }) => {
  const [showDetail, setShowDetail] = useState(false);
  return (
    <>
      <i style={{ color: "red" }}>Error Message: {JSON.stringify(errorMessage)}</i>
      {
        errorStack &&
        <>
          <br />
          <button onClick={() => setShowDetail(!showDetail)}>{showDetail ? "Hide" : "Show"}  Detail</button>
          <br />
          <i hidden={!showDetail}>{JSON.stringify(errorStack)}</i>
        </>
      }
    </>
  )
}

export const ErrorAnimation = ({ errorMessage = "Error isn't provided.", errorStack = "" }) => {
  return (
    <>
      <Lottie
        animationData={ErrorAnimationData}
        autoplay={true}
        loop={false}
        style={{ height: "500px", width: "500px", margin: "0 auto" }}
      />

      <ErrorBoundaryComponent errorMessage={errorMessage} errorStack={errorStack} />
    </>
  );
};


export const ErrorBoundary = () => {
  let error = useRouteError();
  let errorMessage;

  if (isRouteErrorResponse(error)) {
    // error is type `ErrorResponse`
    errorMessage = error.error?.message || error.statusText;
  } else if (error instanceof Error) {
    errorMessage = error.message;
  } else if (typeof error === 'string') {
    errorMessage = error;
  } else {
    console.error(error);
    errorMessage = 'Unknown error';
  }
  return <ErrorAnimation errorMessage={errorMessage} errorStack={error.stack} />
}
