/* eslint-disable import/first */
import { ErrorBoundary } from "@/components/Error";

const APP_VERSION="app"

const privateRoutes = [
  {
    path: `/${APP_VERSION}/public`,
    errorElement: <ErrorBoundary />,
    children: [
      { index: true, element: <>Hello anonymous!</> },
      { path: "*", element: <>public 404!</> },
    ],
  },
]

export default privateRoutes;