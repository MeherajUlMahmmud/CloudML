import React from 'react'
import { Outlet } from 'react-router-dom'

function AuthLayout() {
	return (
		<div className="" style={{
			display: 'flex',
			flexDirection: 'column',
			justifyContent: 'center',
			alignItems: 'center',
			height: '100vh'
		}}>
			<Outlet />
		</div>
	)
}

export default AuthLayout