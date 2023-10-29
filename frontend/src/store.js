import { configureStore } from '@reduxjs/toolkit'
// import { setupListeners } from '@reduxjs/toolkit/query/react'

// middlewares
import { createLogger } from 'redux-logger'

// Reducers and middleware
import rootReducers from './features/index'
import apiSlice from './features/api/apiSlice'
const loggerMiddleware = createLogger({ collapsed: true })
// import { monitorReducersEnhancer } from './middlewares'

const initialState = {};

const store = configureStore({
  reducer: rootReducers,
  middleware: (getDefaultMiddleware) => [...getDefaultMiddleware().concat(apiSlice.middleware, loggerMiddleware)],
  preloadedState: initialState,
  devTools: true, // process.env.NODE_ENV !== 'production',
});

export default store;

// optional, but required for refetchOnFocus/refetchOnReconnect behaviors
// setupListeners(store.dispatch)
