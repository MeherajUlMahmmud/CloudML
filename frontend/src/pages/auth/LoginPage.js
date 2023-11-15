import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { sendAuthRequest } from '../../apis/api';
import { saveStorage } from '../../utils/persistLocalStorage';
import { LOGIN_URL } from '../../utils/urls';


function LoginPage() {
	const navigate = useNavigate();

	const [inputs, setInputs] = useState({
		username: '',
		password: ''
	})
	const [loading, setLoading] = useState(false)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const handleInputChange = (e) => {
		e.persist() // this is to prevent react from pooling all the events together
		setInputs(inputs => ({ ...inputs, [e.target.name]: e.target.value }))
	}

	const handleSubmit = (e) => {
		e.preventDefault()

		setIsError(false)
		setErrorMessage('')
		setLoading(true)

		sendAuthRequest(LOGIN_URL, inputs)
			.then(res => {
				console.log(res);
				setLoading(false)
				// setUsername('')
				// setPassword('')
				// saveStorage("user", res.data.user);
				// saveStorage("tokens", res.data.tokens);
				// navigate("/");
			})
			.catch(err => {
				setLoading(false)
				console.log(err);
				setErrorMessage(err?.message || err?.response?.data?.message || 'Something went wrong!')
				setIsError(true)
			});
	}

	return (
		<div className="container">
			<div className="h-100">
				<div className="text-center m-3">
					<h2>CloudML</h2>
				</div>
				<div className="card p-3 w-50 mx-auto">
					<div className="card-body">
						<h4 className=" text-center">Sign in to start your session</h4>
						<form method="post" onSubmit={(e) => handleSubmit(e)}>
							<div className="mb-3 form-group">
								<label className="col-sm-12 col-form-label">Username</label>
								<div className="col-sm-12">
									<div className="input-group mb-3">
										<span className="input-group-text" id="basic-addon1">@</span>
										<input
											type="text"
											className="form-control"
											placeholder="Username"
											name='username'
											value={inputs.username}
											onChange={(e) => handleInputChange(e)}
											required
											autoFocus
										/>
									</div>
								</div>
							</div>
							<div className="mb-3 form-group">
								<label className="col-sm-12 col-form-label">Password</label>
								<div className="col-sm-12">
									<input
										type="password"
										className="form-control"
										placeholder="Password"
										name='password'
										value={inputs.password}
										onChange={(e) => handleInputChange(e)}
										required
									/>
								</div>
							</div>
							<div className="row">
								<div className="col-lg-12 col-sm-12 text-center">
									<button
										type="submit"
										className="btn btn-primary btn-block"
									>
										{loading ? (
											<div className="spinner-border text-light" role="status">
												<span className="sr-only"></span>
											</div>
										) : (
											'Sign In'
										)}
									</button>
								</div>
							</div>
							{isError && (
								<div className="row mt-2">
									<div className="col-12">
										<div className="alert alert-danger alert-dismissible">
											{errorMessage || 'Something went wrong!'}
										</div>
									</div>
								</div>
							)}
						</form>
						<p className="mb-1 text-center">
							<a href="/auth/forgot-password">I forgot my password</a>
						</p>
					</div>
				</div>
			</div>
		</div>
	)
}

export default LoginPage