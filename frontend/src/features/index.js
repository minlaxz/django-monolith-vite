import emptyApiSlice from '@/features/api/apiSlice'

const rootReducers = ({
  // here your custom reducer goes for local state if you needed to.
  [emptyApiSlice.reducerPath]: emptyApiSlice.reducer
});

export default rootReducers;