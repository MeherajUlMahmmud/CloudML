import React from 'react';
import './TransparentModal.scss'; // Add your modal styles here

const TransparentModal = ({ children, onClose }) => {
	return (
		<div className="modal-overlay">
			<div className="modal-content">
				<button className="close-button" onClick={onClose}>
					X
				</button>
				{children}
			</div>
		</div>
	);
};

export default TransparentModal;
