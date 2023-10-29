import { useRoutes } from "react-router-dom";
import * as routes from "@/routes"


const InternalApp = ({ data }) => {
  let setRoute = null;
  switch (data.redirectRoute) {
    case "privateRoutes":
      setRoute = routes.privateRoutes;
      break;
    case "publicRoutes":
      setRoute = routes.publicRoutes;
      break;
    default:
      setRoute = routes.publicRoutes;
  }

  return (
    <>
      {useRoutes(setRoute)}
    </>
  )
}

const App = () => {
  const data = {redirectRoute: "privateRoutes"}
  return (
    <InternalApp data={data} />
  )
};

export default App;
