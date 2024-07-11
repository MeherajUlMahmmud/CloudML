import React from 'react'
import './Navbar.scss'

function Navbar({ user }) {
	return (
		<div className='navbar'>
			<div className='navbar-container'>
				<div className='navbar-left'>
					<div className='logo'>
						<h1>Logo</h1>
					</div>
				</div>
				<div className='navbar-right'>
					<h3>{user?.first_name} {user?.last_name}</h3>
				</div>
			</div>
		</div>
	)
}

export default Navbar