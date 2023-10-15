import React, { useEffect, useState } from 'react';

function CsvViewer({ csvFile }) {
	const BASE_URL = process.env.REACT_APP_API_URL;
	const filePath = BASE_URL + csvFile;

	const [csvData, setCsvData] = useState('');
	const [splitedData, setSplitedData] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		// read the file from the server
		fetch(filePath)
			.then((response) => response.text())
			.then((text) => {
				setCsvData(text);
				setSplitedData(text?.split('\n').slice(0, 51));
				setLoading(false);
			});
	}, []);

	// const handleFileChange = (event) => {
	// 	const file = event.target.files[0];
	// 	if (file) {
	// 		const reader = new FileReader();
	// 		reader.onload = (e) => {
	// 			setCsvData(e.target.result);
	// 		};
	// 		reader.readAsText(file);
	// 	}
	// };

	return (
		<div>
			{/* <input type="file" onChange={handleFileChange} /> */}
			{
				loading && <div>Loading...</div>
			}
			{
				!loading && !csvData && !splitedData.length > 0 && <div> No data</div>
			}
			{
				!loading && csvData && splitedData.length > 0 &&
				<pre
					style={{
						whiteSpace: 'pre-wrap',
						wordBreak: 'break-word',
						overflowY: 'scroll',
						overflowX: 'scroll',
						maxHeight: '50vh',
					}}
				>
					<>
						<div className='row spaceBetween'>
							{
								splitedData[0].split(',').map((header, index) => {
									return (
										<div key={index} style={{
											border: '1px solid black',
											padding: '5px',
											margin: '5px',
											width: '100px',
											textAlign: 'center',
										}}>
											{header}
										</div>
									);
								}
								)
							}
						</div>
						{
							splitedData.length > 0 && splitedData.slice(1).map((row, index) => {
								return (
									<div className='row '>
										<div key={index} className='row spaceBetween' style={{
											border: '1px solid black',
											margin: '5px',
											width: '100%',
										}} >
											{row.split(',')?.map((data, index) => {
												return (
													<div key={index} style={{
														padding: '5px',
														width: '100px',
														textAlign: 'center',
													}}>
														{data}
													</div>
												);
											})}
										</div>
									</div>
								);
							}
							)
						}

					</>
				</pre>
			}
		</div >
	);
}

export default CsvViewer;
