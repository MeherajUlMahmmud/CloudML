import React, { useEffect } from 'react'
import { logout } from '../../utils/utils'
import { useNavigate } from 'react-router-dom';

function LogoutPage() {
	const navigate = useNavigate();

	useEffect(() => {
		logout(navigate);
	}, [])

	return (
		<div>
			<p>
				Redirecting to login page...
			</p>
		</div>
	)
}

export default LogoutPage