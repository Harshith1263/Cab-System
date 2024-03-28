import React, { useState, useEffect } from 'react';

const CabList = () => {
  const [cabs, setCabs] = useState([]);

  useEffect(() => {
    const fetchCabs = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/cablist/');
        if (!response.ok) {
          throw new Error('Failed to fetch cabs');
        }
        const data = await response.json();
        setCabs(data);
        console.log(data);
      } catch (error) {
        console.error('Error fetching cabs:', error);
      }
    };
    fetchCabs();
  }, []);

  return (
    <div>
      <h2>List of Cabs</h2>
      <ul>
        {cabs.map((cab,index) => (
          <li key={index}>{cab.cab_name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CabList;
