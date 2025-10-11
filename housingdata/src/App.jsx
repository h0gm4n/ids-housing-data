import { useState } from 'react'
import styles from './css/styling.module.css'


const App = () => {

  const [postalCode, setPostalCode] = useState('')
  const [livingSpace, setLivingSpace] = useState('')
  const [apartmentPrice, setApartmentPrice] = useState('')
  const [predictedPrice, setPredictedPrice] = useState('')
  const [predictedLivingSpace, setPredictedLivingSpace] = useState('')
  const [showResultsPrice, setShowResultsPrice] = useState(false)
  const [showResultsLivingSpace, setShowResultsLivingSpace] = useState(false)

  const handlePostalCodeChange = (event) => {
    setPostalCode(event.target.value)
  }

  const handleLivingSpaceChange = (event) => {
    setLivingSpace(event.target.value)
  }

  const handleApartmentPriceChange = (event) => {
    setApartmentPrice(event.target.value)
  }

  /*
  Get values from forms and send to backend
  */
  async function getApartments(event) {
    event.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          postalCode: postalCode,
          livingSpace: livingSpace,
          apartmentPrice: apartmentPrice
        })
      });

      const data = await response.json();
      console.log("Received from backend:", data);
      setPredictedPrice(data['predicted_price'])
      setPredictedLivingSpace(data['predicted_living_space'])
    } catch (error) {
      console.error("Error sending data:", error);
    }
    setShowResultsPrice(true)
    setShowResultsLivingSpace(true)
  }

  const resultsBoxPrice = () => {
    return (
      <div className={styles.resultsStylePrice}>
        <h2>Price Prediction</h2>
        <p>In postal code area</p>
        <p className={styles.bold}>{postalCode}</p>
        <p>You should be able to get an apartment of size</p>
        <p className={styles.bold}>{livingSpace} m2</p>
        <p>For the price of</p>
        <h2 className={styles.bold}>{Math.round(predictedPrice)} €</h2>
      </div>
    )
  }

  const resultsBoxLivingSpace = () => {
    return (
      <div className={styles.resultsStyleLivingSpace}>
        <h2>Living Space Prediction</h2>
        <p>In postal code area</p>
        <p className={styles.bold}>{postalCode}</p>
        <p>For the price of</p>
        <p className={styles.bold}>{apartmentPrice} €</p>
        <p>You should be able to get an apartment of size</p>
        <h2 className={styles.bold}>{Math.round(predictedLivingSpace)} m2</h2>
      </div>
    )
  }

  return (
    <div>
      <h1 className={styles.headerStyle}>Housing Data Analyzer</h1>
      <form className={styles.apartmentFormStyle} onSubmit={getApartments}>
        Postal Code:<br />
        <input value={postalCode} onChange={handlePostalCodeChange} /><br />
        Living Space:<br />
        <input value={livingSpace} onChange={handleLivingSpaceChange} /><br />
        Apartment Price:<br />
        <input value={apartmentPrice} onChange={handleApartmentPriceChange} /><br />
        <button type="submit">Submit</button>
      </form>
      {showResultsPrice ? resultsBoxPrice() : null}
      {showResultsLivingSpace ? resultsBoxLivingSpace() : null}
    </div>
  )
}

export default App
