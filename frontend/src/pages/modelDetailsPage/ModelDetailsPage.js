import React, { useEffect, useState } from 'react'
import './ModelDetailsPage.scss'
import { useOutletContext } from 'react-router-dom'
import { sendGetRequest } from '../../apis/api'
import { formatDateTime, logout } from '../../utils/utils'

function ModelDetailsPage() {
	const projectID = window.location.pathname.split('/')[2]
	const datasetID = window.location.pathname.split('/')[4]
	const modelID = window.location.pathname.split('/')[6]

	const BASE_URL = process.env.REACT_APP_API_URL;

	const [model, setModel] = useState()
	const [loading, setLoading] = useState(true)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const [user, tokens, navigate] = useOutletContext();

	useEffect(() => {
		setLoading(true);

		fetchModelDetails();
	}, [])

	const fetchModelDetails = () => {
		sendGetRequest('/trained-model/' + modelID, tokens?.access)
			.then(res => {
				console.log(res);
				setModel(res?.data)
				setLoading(false)
			})
			.catch(err => {
				setLoading(false)
				setIsError(true)
				setErrorMessage(err?.response?.data?.detail || err?.message || 'Something went wrong')
				console.log(err?.response);
				console.log(err?.response?.status);
				if (err?.response?.status === 401) {
					logout(navigate);
				}
			});
	};

	return (
		<div className='pageContainer'>
			{loading && <h3>Loading...</h3>}
			{isError && <h3>{errorMessage}</h3>}
			{!loading && !isError && (
				<>
					<p className='backLink'>
						<a href='/'>Home</a>
						<span> / </span>
						<a href={'/project/' + projectID}>
							{model?.dataset_model?.project_model?.name}
						</a>
						<span> / </span>
						<span>
							<a href={'/project/' + projectID + '/dataset/' + datasetID}>
								{model?.dataset_model?.name}
							</a>
						</span>
						<span> / </span>
						<span>
							{model?.name}
						</span>
					</p>
					<div className='modelDetails'>
						<div className='topSec'>
							<div className='titleRow'>
								<div className='title'>
									<span>{model?.name}</span>
								</div>
								<div className='action'>
									<a
										href={BASE_URL + model?.model}
										target='_blank'
										rel='noreferrer'
										className='btn btn-primary'
									>
										DOWNLOAD MODEL
									</a>
								</div>
							</div>
							<p className='subtitle'>{model?.description}</p>
							<div className='datetimes'>
								<small>Last Modified At: {formatDateTime(model?.updated_at)}</small>
							</div>
						</div>
						<hr />

						{
							model.metrics && (
								<>
									<div className='section'>
										<div className='sectionTitle'>
											<p>Metrics</p>
										</div>
										<div className='sectionContent'>
											<span>
												{Object.keys(model?.metrics).map((key, index) => (
													<span key={index}>
														<span style={{
															fontWeight: 'bold',
															textTransform: 'uppercase'
														}}>{key}:</span> {model?.metrics[key]}<br />
													</span>
												))}


											</span>
										</div>
									</div>
									<hr />
								</>
							)
						}

						{
							model?.plots && (
								<>
									<div className='section'>
										<div className='sectionTitle'>
											<p>Plots</p>
										</div>
										<div className='sectionContent'>
											<span>
												{

													<div className='grid-3'>
														{Object.keys(model?.plots).map((key, index) => (
															<div key={index} className='col'>
																<p style={{
																	fontWeight: 'bold',
																	textTransform: 'capitalize'
																}}>
																	{key}
																</p>
																<img
																	src={BASE_URL + '/' + model?.plots[key]}
																	alt={key}
																	style={{ width: '300px', height: '300px' }}
																/><br />
															</div>
														))}
													</div>

												}
											</span>
										</div>
									</div>
									<hr />
								</>
							)
						}

					</div>
				</>
			)}
		</div>
	)
}

export default ModelDetailsPage