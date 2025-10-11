import { useState } from 'react'
import styles from './css/styling.module.css'


const App = () => {

  const [postalCode, setPostalCode] = useState('00560')
  const [livingSpace, setLivingSpace] = useState('90')
  const [apartmentPrice, setApartmentPrice] = useState('500000')
  const [predictedPrice, setPredictedPrice] = useState('')
  const [predictedLivingSpace, setPredictedLivingSpace] = useState('')
  const [showResultsPrice, setShowResultsPrice] = useState(false)
  const [showResultsLivingSpace, setShowResultsLivingSpace] = useState(false)
  const [givenPostalCode, setGivenPostalCode] = useState('')
  const [givenLivingSpace, setGivenLivingSpace] = useState('')
  const [givenApartmentPrice, setGivenApartmentPrice] = useState('')
  const [showPostalCodeError, setShowPostalCodeError] = useState(false)
  const [showLivingSpaceError, setShowLivingSpaceError] = useState(false)
  const [showApartmentPriceError, setShowApartmentPriceError] = useState(false)
  const postalCodeText = "In (or near) postal code area"
  const postalCodeError = "Postal code should be 5 characters long and consist of numbers only!"
  const livingSpaceError = "Living space should be an integer or decimal with separator '.'"
  const apartmentPriceError = "Apartment price should be an integer or decimal with separator '.'"

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


  /*
  Validate given values
  */
  const validateValues = () => {
    let postal_code_ok = false
    let living_space_ok = false
    let apartment_price_ok = false
    let regex = /^\d+$/
    if (postalCode.length == 5 && regex.test(postalCode)) {
      postal_code_ok = true
      setShowPostalCodeError(false)
    } else {
      postal_code_ok = false
      setShowPostalCodeError(true)
    }
    if (!isNaN(livingSpace)) {
      living_space_ok = true
      setShowLivingSpaceError(false)
    } else {
      living_space_ok = false
      setShowLivingSpaceError(true)
    }
    if (!isNaN(apartmentPrice)) {
      apartment_price_ok = true
      setShowApartmentPriceError(false)
    } else {
      apartment_price_ok = false
      setShowApartmentPriceError(true)
    }
    if (postal_code_ok == true && living_space_ok == true && apartment_price_ok == true) {
      console.log("OK!")
      return true
    }
    return false
  }

  async function getApartments(event) {
    event.preventDefault()
    const validated = validateValues()
    console.log(validated)
    if (validated == true) {
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
        setGivenPostalCode(data['given_postal_code'])
        setGivenLivingSpace(data['given_living_space'])
        setGivenApartmentPrice(data['given_apartment_price'])
      } catch (error) {
        console.error("Error sending data:", error);
      }
      setShowResultsPrice(true)
      setShowResultsLivingSpace(true)
    } else {
      setShowResultsPrice(false)
      setShowResultsLivingSpace(false)
    }
  }

  const resultsBoxPrice = () => {
    return (
      <div className={styles.resultsStylePrice}>
        <h2>Price Prediction</h2>
        <p>{postalCodeText}</p>
        <p className={styles.bold}>{givenPostalCode}</p>
        <p>You should be able to get an apartment of size</p>
        <p className={styles.bold}>{givenLivingSpace} m2</p>
        <p>For the price of</p>
        <h2 className={styles.bold}>{Math.round(predictedPrice)} €</h2>
      </div>
    )
  }

  const resultsBoxLivingSpace = () => {
    return (
      <div className={styles.resultsStyleLivingSpace}>
        <h2>Living Space Prediction</h2>
        <p>{postalCodeText}</p>
        <p className={styles.bold}>{givenPostalCode}</p>
        <p>For the price of</p>
        <p className={styles.bold}>{givenApartmentPrice} €</p>
        <p>You should be able to get an apartment of size</p>
        <h2 className={styles.bold}>{Math.round(predictedLivingSpace)} m2</h2>
      </div>
    )
  }

  const apartmentValueForm = () => {
    return (
      <div>
        <form className={styles.apartmentFormStyle} onSubmit={getApartments}>
          Postal Code:<br />
          <input value={postalCode} onChange={handlePostalCodeChange} /><br />
          Living Space:<br />
          <input value={livingSpace} onChange={handleLivingSpaceChange} /><br />
          Apartment Price:<br />
          <input value={apartmentPrice} onChange={handleApartmentPriceChange} /><br />
          <button type="submit">Submit</button>
        </form>
      </div>
    )
  }

  return (
    <div>
      <h1 className={styles.headerStyle}>Housing Data Analyzer</h1>
      <p className={styles.validationError}>{showPostalCodeError ? postalCodeError : null}</p>
      <p className={styles.validationError}>{showLivingSpaceError ? livingSpaceError : null}</p>
      <p className={styles.validationError}>{showApartmentPriceError ? apartmentPriceError : null}</p>
      {apartmentValueForm()}
      {showResultsPrice ? resultsBoxPrice() : null}
      {showResultsLivingSpace ? resultsBoxLivingSpace() : null}
    </div>
  )
}

export default App
