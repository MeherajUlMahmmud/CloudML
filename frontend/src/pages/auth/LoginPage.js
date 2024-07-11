import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { saveLocalStorage } from '../../utils/persistLocalStorage';
import { sendAuthRequest } from '../../apis/api';
import { appName } from '../../utils/constants';
import '../../styles/auth.scss';
import { LOGIN_URL } from '../../utils/urls';
import { forgotPasswordRoute, signUpRoute } from '../../utils/app_routes';
import Button from '../../components/Button';
import ErrorMessage from '../../components/ErrorMessage';

function LoginPage() {
	const [loginData, setLoginData] = useState({
		email: '',
		password: ''
	});
	const [loading, setLoading] = useState(false)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const navigate = useNavigate();

	const handleChangeLoginData = (e) => {
		const { name, value } = e.target;
		setLoginData({
			...loginData,
			[name]: value
		})
	};

	const handleSubmit = (e) => {
		e.preventDefault();

		setIsError(false);
		setErrorMessage('');
		setLoading(true);

		sendAuthRequest(LOGIN_URL, loginData)
			.then(res => {
				console.log(res);
				setLoading(false)

				saveLocalStorage("user", res.data.user);
				saveLocalStorage("tokens", res.data.tokens);
				navigate('/');
			})
			.catch(err => {
				setLoading(false);
				// console.log(err?.response);
				// console.log(err?.response?.status);
				setErrorMessage(err?.response?.data?.detail)
				setIsError(true)
			});
	};

	return (
		<div className="authContainer">
			<div className="loginPage">
				<div className="headerSection">
					<h1>{appName}</h1>
					<h3>
						Sign in to start your session
					</h3>
				</div>
				<form method="post" className='loginForm' onSubmit={!loading && handleSubmit}>
					<div className="inputField">
						<input
							type="email"
							className="input"
							placeholder="Email Address"
							name="email"
							onChange={(e) => handleChangeLoginData(e)}
							required
							autoFocus
						/>
					</div>
					<div className="inputField">
						<input
							type="password"
							className="input"
							placeholder="Password"
							name="password"
							onChange={(e) => handleChangeLoginData(e)}
							required
						/>
					</div>

					<small className="">
						<a href={forgotPasswordRoute}>
							Forgot your password?
						</a>
					</small>
					{
						!loading && isError && <ErrorMessage errorMessage={errorMessage} />
					}

					<div className="actionsSection">
						<Button
							text={loading ? 'Loading...' : 'Sign In'}
							type={"submit"}
							isDisabled={loading}
							className={`button ${loading && 'disabled'}`}
						/>
					</div>
				</form>

				<small className="">
					<a href={signUpRoute} className=''>
						Don't have an account? Sign Up
					</a>
				</small>
			</div>
		</div>
	)
}

export default LoginPage