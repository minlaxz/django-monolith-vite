import emptyApiSlice from '@/features/api/apiSlice'
import { createSlice, createSelector } from '@reduxjs/toolkit'

const initialState = {
  data: null,
  error: null,
  status: 'idel',
}

const slice = createSlice({
  name: "onAuth",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addMatcher(
      onAuthApiSlice.endpoints.getOnAuth.matchFulfilled,
      (state, { payload }) => {
        state.data = payload
        state.error = null
      }
    )
  }
})
export default slice.reducer
export const selectOnAuth = (state) => state.onAuth.data


export const onAuthApiSlice = emptyApiSlice.injectEndpoints({
  endpoints: builder => ({
    getOnAuth: builder.query({
      query: () => '/users/auth/?edge-migration=1',
      transformResponse: responseData => responseData,
    }),
  })
})

export const { useGetOnAuthQuery } = onAuthApiSlice
export const _selectOnAuthResult = onAuthApiSlice.endpoints.getOnAuth.select()

export const selectOnAuthResult = createSelector(
  _selectOnAuthResult,
  onAuthResult => onAuthResult?.data
)
export const selectOnAuthUserInfoResult = createSelector(
  _selectOnAuthResult,
  onAuthResult => onAuthResult?.data?.userInfo
)

export const selectOnAuthTeamInfoResult = createSelector(
  _selectOnAuthResult,
  onAuthResult => onAuthResult?.data?.teamInfo
)

export const selectOnAuthRedirectRouteResult = createSelector(
  _selectOnAuthResult,
  onAuthResult => onAuthResult?.data?.redirectRoute
)
