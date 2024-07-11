import React from 'react';
import '../styles/button.scss';

const Button = ({ text, type, className, isDisabled = false, onClick }) => {
	return (
		<button
			type={type}
			className={className}
			disabled={isDisabled}
			onClick={onClick}
		>
			<span dangerouslySetInnerHTML={{ __html: text }} />
		</button>
	)
}

export default Button;
