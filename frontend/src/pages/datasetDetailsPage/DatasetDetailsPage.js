import React, { useEffect, useState } from 'react'
import './DatasetDetailsPage.scss'
import { useOutletContext } from 'react-router-dom'
import { sendDeleteRequest, sendGetRequest, sendPatchRequest, sendPostRequest } from '../../apis/api'
import { formatDateTime, logout } from '../../utils/utils'
import TransparentModal from '../../components/transparentModal/TransparentModal'
import CsvViewer from '../../components/csvViewer/CSVViewer'

function DatasetDetailsPage() {
	const projectID = window.location.pathname.split('/')[2]
	const datasetID = window.location.pathname.split('/')[4]
	const BASE_URL = process.env.REACT_APP_API_URL;

	const [dataset, setDataset] = useState({})
	const [columns, setColumns] = useState([])
	const [trainedModels, setTrainedModels] = useState([])
	const [loading, setLoading] = useState(true)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
	const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

	const [user, tokens, navigate] = useOutletContext();

	useEffect(() => {
		setLoading(true);

		fetchDatasetDetails();
	}, [])

	const fetchDatasetDetails = () => {
		sendGetRequest('/dataset/' + datasetID, tokens?.access)
			.then(res => {
				console.log(res);
				setDataset(res?.data['dataset'])
				setColumns(res?.data['columns'])
				fetchModels();
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

	const fetchModels = () => {
		sendGetRequest('/trained-model/?dataset_model=' + datasetID, tokens?.access)
			.then(res => {
				console.log(res);
				setTrainedModels(res?.data)
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

	const deleteDataset = () => {
		if (window.confirm('Are you sure you want to delete this dataset?')) {
			setLoading(true);
			sendDeleteRequest('/dataset/' + datasetID, tokens?.access)
				.then(res => {
					console.log(res);
					setLoading(false)
					navigate('/project/' + projectID)
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
		}
	};

	const downloadDataset = () => {
		// const element = document.createElement("a");
		// const file = new Blob(BASE_URL + dataset?.dataset, { type: 'text/csv' });
		// element.href = URL.createObjectURL(file);
		// element.download = dataset?.name + '.csv';
		// document.body.appendChild(element); // Required for this to work in FireFox
		// element.click();

		window.open(BASE_URL + dataset?.dataset, '_blank');
	};

	const updateColumns = () => {
		setLoading(true);
		if (validateColumns() === false) {
			setLoading(false)
			return
		}

		sendPatchRequest('/column/update-columns/' + datasetID, { columns }, tokens?.access)
			.then(res => {
				console.log(res);
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

	const validateColumns = () => {
		let targetCount = 0
		let isFeatureAndTarget = false
		columns.forEach((column) => {
			if (column.is_target) {
				targetCount += 1
			}
			if (column.is_target && column.is_feature) {
				isFeatureAndTarget = true
			}
		}
		)
		if (isFeatureAndTarget) {
			alert('A column cannot be both feature and target')
			return false
		}
		if (targetCount > 1) {
			alert('Only one target column can be selected')
			return false
		}
		return true
	}

	return (
		<>
			<div className='pageContainer'>
				{loading && <h3>Loading...</h3>}
				{isError && <h3>{errorMessage}</h3>}
				{!loading && !isError && (
					<>
						<p className='backLink'>
							<a href='/'>Home</a>
							<span> / </span>
							<a href={'/project/' + projectID}>
								{dataset?.project_model?.name}
							</a>
							<span> / </span>
							<a href={'/project/' + projectID}>Datasets</a>
							<span> / </span>
							<span>
								{dataset?.name}
							</span>
						</p>
						<div className='datasetDetails'>
							<div className='topSec'>
								<div className='titleRow'>
									<div className='title'>
										<span>{dataset?.name}</span>
									</div>
									<div className='action'>
										<button
											className='btn btn-primary'
											onClick={() => {
												setIsUpdateModalOpen(true)
											}}
										>
											Update
										</button>
										<button
											className='btn btn-danger'
											onClick={() => {
												deleteDataset()
											}}
										>
											Delete
										</button>
									</div>
								</div>
								<p className='subtitle'>{dataset?.description}</p>
								<div className='datetimes'>
									{/* <small>Created At: {formatDateTime(project?.created_at)}</small> */}
									<small>Last Modified At: {formatDateTime(dataset?.updated_at)}</small>
								</div>
							</div>
							<hr />

							<div className='section'>
								<div className='sectionTitle'>
									<p>
										Dataset Preview
									</p>
									<button
										className='btn btn-primary'
										onClick={() => downloadDataset()}>
										Download Dataset
									</button>
								</div>
								<div className='sectionContent'>
									<CsvViewer csvFile={dataset?.dataset} />
								</div>
							</div>
							<hr />

							<div className='section'>
								<div className='sectionTitle'>
									<p>Columns</p>
								</div>
								<div className='sectionContent'>
									{
										columns.length === 0 && <h3>No columns found</h3>
									}
									<div>
										<div className='sectionItem heading'>
											<div className='col'>
												Column Name
											</div>
											<div className='col'>
												Feature/Target
											</div>
											<div className='col'>
												Datatype
											</div>
											<div className='col'>
												Encoding/Scaling
											</div>
										</div>
										{
											columns?.map((column, index) => (
												<div key={index} className='sectionItem'>
													<div className='col'>
														{/* {column?.name} */}
														<input
															type="text"
															value={column?.name}
															onChange={(e) => {
																setColumns(columns.map((col, i) => {
																	if (i === index) {
																		col.name = e.target.value
																	}
																	return col
																}))
															}}
														/>
													</div>
													<div className='col columnType'>
														<div className='feature'>
															<input
																type="checkbox"
																checked={column?.is_feature}
																onChange={() => {
																	setColumns(columns.map((col, i) => {
																		if (i === index) {
																			col.is_feature = !col.is_feature
																		}
																		return col
																	}))
																}}
															/> Feature
														</div>
														<div className='target'>
															<input
																type="checkbox"
																checked={column?.is_target}
																onChange={() => {
																	setColumns(columns.map((col, i) => {
																		if (i === index) {
																			col.is_target = !col.is_target
																		}
																		return col
																	}))
																}}
															/> Target
														</div>
													</div>
													<div className='col'>
														<select
															defaultValue={column?.is_numeric ? "float" : "string"}
															onChange={(e) => {
																setColumns(columns.map((col, i) => {
																	if (i === index) {
																		col.is_numeric = e.target.value === "float"
																	}
																	return col
																}))
															}}
														>
															<option
																value=""
																disabled
															>
																Select Datatype
															</option>
															<option value="float">Numerical</option>
															<option value="string">Categorical</option>
														</select>
													</div>
													{
														column?.is_numeric && (
															<div className='col'>
																<select
																	defaultValue={column?.scaling_type}
																	onChange={(e) => {
																		setColumns(columns.map((col, i) => {
																			if (i === index) {
																				col.scaling_type = e.target.value
																			}
																			return col
																		}))
																	}}
																>
																	<option value="">Select Scaling</option>
																	<option value="STANDARD">
																		Standard Scaler
																	</option>
																	<option value="MIN_MAX">
																		Min Max Scaler
																	</option>
																	<option value="MAX_ABS">
																		Max Abs Scaler
																	</option>
																	<option value="ROBUST">
																		Robust Scaler
																	</option>
																</select>
															</div>
														)
													}
													{
														!column?.is_numeric && (
															<div className='col'>
																<select>
																	<option value="">Select Encoding</option>
																	<option value="ONE_HOT">
																		One Hot Encoding
																	</option>
																</select>
															</div>
														)
													}
												</div>
											))}
									</div>
									<div className='sectionFooter'>
										<button
											className='btn btn-primary'
											onClick={() => {
												updateColumns()
											}}
										>
											Update Columns
										</button>
									</div>
								</div>
							</div>
							<hr />

							<div className='modelSection'>
								<div className='sectionTitle'>
									<p>Training</p>
									<button
										className='btn btn-primary'
										onClick={() => setIsCreateModalOpen(true)}>
										Train New Model
									</button>
								</div>
								<div className='sectionContent'>
									{
										trainedModels.length === 0 && <h3>No trained models found</h3>
									}
									{
										trainedModels?.map((model, index) => (
											<div key={index} className='model'>
												<div className='title'>
													<span>
														{model?.name}
													</span>
													<div className='actions'>
														<a
															className='btn btn-primary'
															href={'/project/' + projectID + '/dataset/' + datasetID + '/trained-model/' + model?.id}
														>
															View Model Details
														</a>
													</div>
												</div>
												<span>
													{model?.description}
												</span>
												<span>
													Model Type: {model?.model_type}
												</span>
												<span>
													{model?.is_training ? 'Training' : 'Training Completed'}
												</span>
												<span>
													{
														model?.metrics && (
															<>
																<hr />
																<p>
																	Metrics:
																</p>
																{Object.keys(model?.metrics).map((key, index) => (
																	<span key={index}>
																		{key}: {model?.metrics[key]}<br />
																	</span>
																))}
															</>
														)
													}
												</span>
											</div>
										))}
								</div>
							</div>

						</div>
					</>
				)
				}
			</div>
			{
				isUpdateModalOpen && (
					<TransparentModal onClose={() => setIsUpdateModalOpen(false)}>
						<UpdateDatasetForm
							tokens={tokens}
							navigate={navigate}
							projectID={projectID}
							datasetID={datasetID}
							dataset={dataset}
							setIsUpdateModalOpen={setIsUpdateModalOpen}
							fetchDatasetDetails={fetchDatasetDetails}
						/>
					</TransparentModal>
				)
			}
			{
				isCreateModalOpen && (
					<TransparentModal onClose={() => setIsCreateModalOpen(false)}>
						<CreateModelForm
							tokens={tokens}
							navigate={navigate}
							projectID={projectID}
							datasetID={datasetID}
							setIsCreateModalOpen={setIsCreateModalOpen}
							fetchModels={fetchModels}
						/>
					</TransparentModal>
				)
			}
		</>
	)
}

function UpdateDatasetForm({ tokens, navigate, projectID, datasetID, dataset, setIsUpdateModalOpen, fetchDatasetDetails }) {
	const [name, setName] = useState(dataset?.name)
	const [description, setDescription] = useState(dataset?.description)
	const [loading, setLoading] = useState(false)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')
	const [isSuccess, setIsSuccess] = useState(false)

	const handleSubmit = (e) => {
		e.preventDefault()

		setLoading(true)
		setIsError(false)
		setIsSuccess(false)

		sendPatchRequest('/dataset/' + datasetID + '/', { name, description }, tokens?.access)
			.then(res => {
				console.log(res);
				setLoading(false)
				setIsSuccess(true)
				setIsUpdateModalOpen(false)
				fetchDatasetDetails()
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
	}

	return (
		<div className='form'>
			<h3 className='formTitle'>Update Dataset</h3>
			<form className='formContent' onSubmit={handleSubmit}>
				<div className='formItem'>
					<label htmlFor='name' className='formLabel'>Name</label>
					<input
						className='formInput'
						type='text'
						id='name'
						placeholder='Enter name'
						value={name}
						onChange={(e) => setName(e.target.value)}
						required
					/>
				</div>
				<div className='formItem'>
					<label htmlFor='description' className='formLabel'>Description</label>
					<textarea
						className='formInput'
						id='description'
						placeholder='Enter description'
						value={description}
						onChange={(e) => setDescription(e.target.value)}
					/>
				</div>
				<div className='formAction'>
					<button
						type='submit'
						className='btn btn-primary'
						disabled={loading}
					>
						{loading ? 'Updating...' : 'Update'}
					</button>
					<button
						type='button'
						className='btn btn-secondary'
						onClick={() => setIsUpdateModalOpen(false)}
					>
						Cancel
					</button>
				</div>
				{isError && <p className='error'>{errorMessage}</p>}
				{isSuccess && <p className='success'>Project updated successfully</p>}
			</form>
		</div>
	)

}

function CreateModelForm({ tokens, navigate, projectID, datasetID, setIsCreateModalOpen, fetchModels }) {
	const [name, setName] = useState('')
	const [description, setDescription] = useState('')
	const [type, setType] = useState('LINEAR_REGRESSION')
	const [testSize, setTestSize] = useState(0.2)
	const [loading, setLoading] = useState(false)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')
	const [isSuccess, setIsSuccess] = useState(false)

	const handleSubmit = (e) => {
		e.preventDefault()

		setLoading(true)
		setIsError(false)
		setIsSuccess(false)

		const data = {
			name,
			description,
			model_type: type,
			project_model: projectID,
			dataset_model: datasetID,
			test_size: testSize
		}

		sendPostRequest('/trained-model/', data, tokens?.access)
			.then(res => {
				console.log(res);
				setLoading(false)
				setIsSuccess(true)
				setIsCreateModalOpen(false)
				fetchModels()
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
	}

	return (
		<div className='createModelForm'>
			<h3 className='formTitle'>Create New Model</h3>
			<form className='formContent' onSubmit={handleSubmit}>
				<div className='formItem'>
					<label htmlFor='name' className='formLabel'>Name</label>
					<input
						className='formInput'
						type='text'
						id='name'
						placeholder='Enter name'
						value={name}
						onChange={(e) => setName(e.target.value)}
						required
					/>
				</div>
				<div className='formItem'>
					<label htmlFor='description' className='formLabel'>Description</label>
					<textarea
						className='formInput'
						id='description'
						placeholder='Enter description'
						value={description}
						onChange={(e) => setDescription(e.target.value)}
					/>
				</div>
				<div className='formItem'>
					<label htmlFor='description' className='formLabel'>Type</label>
					<select
						className='formInput'
						id='type'
						value={type}
						onChange={(e) => setType(e.target.value)}
						required
					>
						<option value="">Select Type</option>
						<option value="LINEAR_REGRESSION">
							Linear Regression
						</option>
						<option value="LOGISTIC_REGRESSION">
							Logistic Regression
						</option>
						<option value="DECISION_TREE">
							Decision Tree
						</option>
						<option value="RANDOM_FOREST">
							Random Forest
						</option>
						<option value="SUPPORT_VECTOR_MACHINE">
							Support Vector Machine
						</option>
						<option value="K_NEAREST_NEIGHBORS">
							K Nearest Neighbors
						</option>
						<option value="NAIVE_BAYES">
							Naive Bayes
						</option>
						<option value="K_MEANS">
							K Means
						</option>
					</select>
				</div>
				<div className='formItem'>
					<label htmlFor='testSize' className='formLabel'>Test Size</label>
					<input
						className='formInput'
						type='number'
						id='testSize'
						placeholder='Enter test size'
						value={testSize}
						onChange={(e) => setTestSize(e.target.value)}
						required
					/>
				</div>
				<div className='formAction'>
					<button
						type='submit'
						className='btn btn-primary'
						disabled={loading}
					>
						{loading ? 'Creating...' : 'Create'}
					</button>
					<button
						type='button'
						className='btn btn-secondary'
						onClick={() => setIsCreateModalOpen(false)}
					>
						Cancel
					</button>
				</div>
				{isError && <p className='error'>{errorMessage}</p>}
				{isSuccess && <p className='success'>Project created successfully</p>}
			</form>
		</div>
	)
}

export default DatasetDetailsPage