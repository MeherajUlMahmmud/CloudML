import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { saveStorage } from '../../utils/persistLocalStorage';
import { sendAuthRequest } from '../../apis/api';

function LoginPage() {
	const [username, setUsername] = useState('')
	const [password, setPassword] = useState('')
	const [loading, setLoading] = useState(false)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const navigate = useNavigate();

	const handleSubmit = (e) => {
		e.preventDefault()

		setIsError(false)
		setErrorMessage('')
		setLoading(true)

		const user = {
			username: username,
			password: password
		}

		sendAuthRequest('/api/auth/login/', user)
			.then(res => {
				console.log(res.data);
				setLoading(false)
				setUsername('')
				setPassword('')
				saveStorage("user", res.data.user);
				saveStorage("tokens", res.data.tokens);
				navigate("/");
			})
			.catch(err => {
				setLoading(false)
				console.log(err);
				console.log(err?.response);
				console.log(err?.response?.status);
				setErrorMessage(err?.response?.data?.detail || 'Something went wrong!')
				setIsError(true)
			});
	}

	return (
		<div className="login-box">
			<div className="login-logo">
				<b>Pristine Facilities</b>
			</div>
			<div className="card">
				<div className="card-body login-card-body">
					<p className="login-box-msg">Sign in to start your session</p>

					<form method="post" onSubmit={!loading && handleSubmit}>
						<div className="input-group mb-3">
							<input
								type="text"
								className="form-control"
								placeholder="Username"
								value={username}
								onChange={(e) => setUsername(e.target.value)}
								required
								autoFocus
							/>
							<div className="input-group-append">
								<div className="input-group-text">
									<span className="fas fa-user"></span>
								</div>
							</div>
						</div>
						<div className="input-group mb-3">
							<input
								type="password"
								className="form-control"
								placeholder="Password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
								required
							/>
							<div className="input-group-append">
								<div className="input-group-text">
									<span className="fas fa-lock"></span>
								</div>
							</div>
						</div>
						<div className="row">
							<div className="col-4">
							</div>
							<div className="col-4">
								<button
									type="submit"
									className="btn btn-primary btn-block"
								>
									{
										loading ?
											<div className="spinner-border text-light" role="status">
												<span className="sr-only">Loading...</span>
											</div>
											:
											'Sign In'
									}
								</button>
							</div>
							<div className="col-4">
							</div>
						</div>
						{
							isError &&
							<div className="row mt-2">
								<div className="col-12">
									<div className="alert alert-danger alert-dismissible">
										{errorMessage}
									</div>
								</div>
							</div>
						}
					</form>

					<p className="mb-1">
						<a href="/auth/forgot-password">I forgot my password</a>
					</p>
				</div>
			</div>
		</div>
	)
}

export default LoginPage