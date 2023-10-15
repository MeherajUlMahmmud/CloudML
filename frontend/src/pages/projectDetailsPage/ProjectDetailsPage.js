import React, { useEffect, useState } from 'react'
import './ProjectDetailsPage.scss'
import { sendGetRequest, sendPostRequest } from '../../apis/api'
import { useOutletContext } from 'react-router-dom'
import { formatDateTime, logout } from '../../utils/utils'
import TransparentModal from '../../components/transparentModal/TransparentModal'

function ProjectDetailsPage() {
	const projectID = window.location.pathname.split('/').pop()

	const [project, setProject] = useState()
	const [datasets, setDatasets] = useState([])
	const [loading, setLoading] = useState(true)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

	const [user, tokens, navigate] = useOutletContext();

	useEffect(() => {
		setLoading(true);

		fetchProjectDetails();
	}, [])

	const fetchProjectDetails = () => {
		sendGetRequest('/project/' + projectID, tokens?.access)
			.then(res => {
				console.log(res);
				setProject(res?.data['project'])
				setDatasets(res?.data['datasets'])
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
		<>
			<div className='pageContainer'>
				{loading && <h3>Loading...</h3>}
				{isError && <h3>{errorMessage}</h3>}
				{
					!loading && !isError && (
						<>
							<p className='backLink'>
								<a href='/'>Home</a>
								<span> / </span>
								<span>{project?.name}</span>
							</p>
							<div className='projectDetails'>
								<div className='topSec'>
									<p className='title'>{project?.name}</p>
									<p className='subtitle'>{project?.description}</p>
									<div className='datetimes'>
										{/* <small>Created At: {formatDateTime(project?.created_at)}</small> */}
										<small>Last Modified At: {formatDateTime(project?.updated_at)}</small>
									</div>
								</div>
								<hr />
								{/* Datasets */}
								<div className='section' id='datasets'>
									<div className='sectionTitle'>
										<p>Datasets</p>
										<button
											className='btn btn-primary'
											onClick={() => setIsCreateModalOpen(true)}
										>
											Create Dataset
										</button>
									</div>
									<div className='sectionContent'>
										{
											datasets.length === 0 && <h3>No datasets found</h3>
										}
										{
											datasets?.map((dataset, index) => (
												<div key={index} className='sectionItem'>
													<div>
														<p className='itemTitle'>
															{dataset?.name}
														</p>
														<p className='itemSubtitle'>{dataset?.description}</p>
														{dataset?.dataset_size &&
															<p className='itemSubtitle'>Dataset Size: {dataset?.dataset_size} MB</p>}
														<small style={{
															marginTop: '10px',
															color: 'gray',
														}}>
															Created At: {formatDateTime(dataset?.created_at)}
														</small>
													</div>
													<div>
														<a href={'/project/' + projectID + '/dataset/' + dataset?.id} className='btn'
														>
															View Dataset Details
														</a>
													</div>
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
				isCreateModalOpen && (
					<TransparentModal onClose={() => setIsCreateModalOpen(false)}>
						<CreateDatasetForm
							tokens={tokens}
							navigate={navigate}
							projectID={projectID}
							setIsCreateModalOpen={setIsCreateModalOpen}
							fetchProjectDetails={fetchProjectDetails}
						/>
					</TransparentModal>
				)
			}
		</>
	)
}


function CreateDatasetForm({ tokens, navigate, projectID, setIsCreateModalOpen, fetchProjectDetails }) {
	const [name, setName] = useState('')
	const [description, setDescription] = useState('')
	const [datasetFile, setDatasetFile] = useState(null)
	const [loading, setLoading] = useState(false)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')
	const [isSuccess, setIsSuccess] = useState(false)

	const handleSubmit = (e) => {
		e.preventDefault()

		setLoading(true)
		setIsError(false)
		setIsSuccess(false)

		let formData = new FormData();
		formData.append('name', name);
		formData.append('description', description);
		formData.append('dataset', datasetFile);
		formData.append('project_model', projectID);

		sendPostRequest('/dataset/', formData, tokens?.access, true)
			.then(res => {
				console.log(res);
				setLoading(false)
				setIsSuccess(true)
				setIsCreateModalOpen(false)
				navigate('/project/' + projectID + '/dataset/' + res?.data?.id)
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
		<div className='createDatasetForm'>
			<h3 className='formTitle'>Upload a New Dataset</h3>
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
					<label htmlFor='dataset' className='formLabel'>Dataset</label>
					<input
						className='formInput'
						type='file'
						id='dataset'
						placeholder='Select dataset'
						onChange={(e) => setDatasetFile(e.target.files[0])}
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

export default ProjectDetailsPage