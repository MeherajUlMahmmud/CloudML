import React, { useEffect } from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import { loadStorage } from '../utils/persistLocalStorage'
import { isAuthenticated, logout } from '../utils/utils'
import Navbar from './navbar/Navbar';

function AppLayout() {
	var user = loadStorage("user");
	var tokens = loadStorage("tokens");

	const navigate = useNavigate();

	useEffect(() => {
		user = loadStorage("user");
		tokens = loadStorage("tokens");
		if (!isAuthenticated(user, tokens)) {
			console.log("User not authenticated");
			const currentUrl = window.location.pathname;
			logout(navigate, currentUrl);
		}
	}, [])

	return (
		<div
			style={{
				display: 'flex',
				flexDirection: 'column',
				// alignItems: 'center',
				// justifyContent: 'center',
				width: '100vw',
				height: '100vh',
				// padding: '20px',
			}}
		>
			<Navbar user={user} />
			<Outlet
				context={[user, tokens, navigate]}
			/>
		</div>
	)
}

export default AppLayout