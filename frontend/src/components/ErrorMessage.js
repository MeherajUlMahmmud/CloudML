import React from 'react'

function ErrorMessage({ errorMessage }) {
	return (
		<div className='errorMessageContainer'>
			<p className='errorMessage'>{errorMessage || ''}</p>
		</div>
	)
}

export default ErrorMessage