import React, { useEffect, useState } from 'react'
import './HomePage.scss'
import { sendGetRequest, sendPostRequest } from '../../apis/api'
import { useOutletContext } from 'react-router-dom'
import { formatDateTime, logout } from '../../utils/utils'
import TransparentModal from '../../components/transparentModal/TransparentModal'

function HomePage() {
	const [projects, setProjects] = useState([])
	const [loading, setLoading] = useState(true)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

	const [user, tokens, navigate] = useOutletContext();

	useEffect(() => {
		setLoading(true);

		fetchProjects();
	}, [])

	const fetchProjects = () => {
		sendGetRequest('/project/', tokens?.access)
			.then(res => {
				console.log(res);
				setProjects(res?.data)
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
				<div className='pageTitle'>
					<span className='title'>{user?.first_name}'s Projects</span>
					<button
						className='btn btn-primary'
						onClick={() => setIsCreateModalOpen(true)}
					>
						Create Project
					</button>
				</div>
				{loading && <h3>Loading...</h3>}
				{isError && <h3>{errorMessage}</h3>}
				{!loading && !isError && (
					<div className='dataContainer'>
						{
							projects.length === 0 && <h3>No projects found</h3>
						}
						{
							projects?.map((project) => (
								<ProjectCard
									key={project.id}
									project={project}
								/>
							))
						}
					</div>
				)}
			</div>
			{
				isCreateModalOpen && (
					<TransparentModal onClose={() => setIsCreateModalOpen(false)}>
						<CreateProjectForm
							user={user}
							tokens={tokens}
							navigate={navigate}
							setIsCreateModalOpen={setIsCreateModalOpen}
							fetchProjects={fetchProjects}
						/>
					</TransparentModal>
				)
			}
		</>
	)
}

function CreateProjectForm({ user, tokens, navigate, setIsCreateModalOpen, fetchProjects }) {
	const [name, setName] = useState('')
	const [description, setDescription] = useState('')
	const [loading, setLoading] = useState(false)
	const [isError, setIsError] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')
	const [isSuccess, setIsSuccess] = useState(false)

	const handleSubmit = (e) => {
		e.preventDefault()

		setLoading(true)
		setIsError(false)
		setIsSuccess(false)

		sendPostRequest('/project/', { name, description, user: user.id }, tokens?.access)
			.then(res => {
				console.log(res);
				setLoading(false)
				setIsSuccess(true)
				setIsCreateModalOpen(false)
				fetchProjects()
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
		<div className='createProjectForm'>
			<h3 className='formTitle'>Create Project</h3>
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

function ProjectCard({ project = null }) {
	return (
		<div className='projectCard'>
			<a href={'/project/' + project?.id} className='cardContent'>
				<p>{project?.name}</p>
				<p>{project?.description}</p>
				<small>Created At: {formatDateTime(project?.created_at)}</small>
			</a>
		</div>
	)
}

export default HomePage