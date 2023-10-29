import Lottie from "lottie-react";
import pageLoadingData from "@/assets/pageLoadingEdge.json";
import componentLoadingData from "@/assets/componentLoading.json";

const PageLoadingAnimation = ({ infoMessage }) => {
  return (
    <div style={{
      position: "absolute",
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      height: "100%",
      width: "100%",
      backgroundColor: "rgba(0, 0, 0, 0.2)",
      zIndex: 100
    }}
    >
      <Lottie
        animationData={pageLoadingData}
        autoplay={true}
        loop={true}
        style={{ height: "95%", width: "300px", margin: "0 auto" }} />
      <pre style={{ float: "right" }}>{infoMessage || "Loading..."}</pre>
    </div>
  );
};

const InternalLoadingComponent = ({ text = "Loading ...", internalStyle }) => {
  return (
    <div style={{
      display: "flex",
      width: "80vw",
      height: "10vh",
      justifyContent: "center",
      alignContent: "center",
      textAlign: "center",
      ...internalStyle
    }}>
      <div>
        <span style={{ fontSize: "16px" }}> {text} </span>
        <Lottie
          animationData={componentLoadingData}
          autoplay={true}
          loop={true}
          style={{ height: "100%", width: "400px", margin: "0 auto" }}
        />
      </div>
    </div>
  );
};

const SmallLoadingComponent = ({ text = "Fetching data ...", internalStyle }) => {
  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      alignContent: "center",
      textAlign: "center",
      ...internalStyle
    }}>
      <div>
        {
          text ?
            <span style={{ fontSize: "16px" }}> {text} </span>
            : null
        }
        <Lottie
          animationData={componentLoadingData}
          autoplay={true}
          loop={true}
          style={{ height: "100%", width: "300px", margin: "0 auto" }} />
      </div>
    </div>
  );
};

const TooSmallLoadingComponent = ({ text = null, internalStyle }) => {
  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      alignContent: "center",
      textAlign: "center",
      ...internalStyle
    }}>
      <div>
        {
          text ?
            <span style={{ fontSize: "12px" }}> {text} </span>
            : null
        }
        <Lottie
          animationData={componentLoadingData}
          autoplay={true}
          loop={true}
          style={{ height: "100%", width: "100px", margin: "0 auto" }} />
      </div>
    </div>
  );
};


const ComponentLoadingAnimation = (props) => {
  if (props.isLoading) {
    if (props.timedOut) {
      return <div>
        <h5>
          Taking a long time...
        </h5>
        <button onClick={props.retry}>Retry</button>
      </div>;
    } else if (props.pastDelay) {
      return (
        <InternalLoadingComponent text={props?.loadingText ?? "Please wait..."} internalStyle={props.internalStyle} />
      );
    } else {
      return null;
    }
  } else if (props.error) {
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        {/* {console.log(JSON.stringify(props.error))} */}
        <p style={{ color: "red" }}>
          Error! Component failed to load.
        </p>
        <h5>
          {props.error.code}
        </h5>
        <button onClick={props.retry} style={{ margin: "5px", padding: "5px", width: "100px" }}>Retry</button>
      </div>
    );
  } else {
    return (
      <InternalLoadingComponent text="Loading Data, please wait ..." internalStyle={props.internalStyle} />
    );
  }
};

export default PageLoadingAnimation;
export { ComponentLoadingAnimation, SmallLoadingComponent, TooSmallLoadingComponent };