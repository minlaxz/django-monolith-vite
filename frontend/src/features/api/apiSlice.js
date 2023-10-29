import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const emptyApiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/',
    prepareHeaders: (headers, { getState }) => {
      headers.set('X-FE', true)
      return headers;
    }
  }),
  keepUnusedDataFor: 60, // in seconds specifies how long the data should be kept in the cache after the subscriber reference count reaches zero.
  // refetchOnFocus: true,
  // refetchOnMountOrArgChange: true,
  endpoints: builder => ({})
})


export default emptyApiSlice;