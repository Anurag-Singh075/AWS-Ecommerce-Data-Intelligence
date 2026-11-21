
import { useEffect, useState } from 'react'
import './Sellers.css'

const API_URL = 'http://127.0.0.1:8000/api/v1'

function Sellers() {
  const [sellers, setSellers] = useState([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const limit = 20

  const fetchSellers = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch(
        `${API_URL}/sellers/?skip=${skip}&limit=${limit}`
      )

      if (!response.ok) {
        throw new Error('Failed to fetch sellers')
      }

      const data = await response.json()

      setSellers(data.sellers || [])
      setTotal(data.total || 0)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSellers()
  }, [skip])

  const formatCity = (city) => {
    return city
      ? city.replace(/\b\w/g, char => char.toUpperCase())
      : '—'
  }

  return (
    <div className="sellers-page">
      <div className="page-header">
        <div>
          <h2>Sellers</h2>
          <p>Explore seller information and locations.</p>
        </div>
        <button className="refresh-btn" onClick={fetchSellers}>
          ↻ Refresh
        </button>
      </div>

      <div className="sellers-summary">
        <div className="sellers-summary-card">
          <span>Total Sellers</span>
          <h2>{total.toLocaleString('en-IN')}</h2>
        </div>

        <div className="sellers-summary-card">
          <span>Showing Sellers</span>
          <h2>{sellers.length}</h2>
        </div>

        <div className="sellers-summary-card">
          <span>Current Page</span>
          <h2>{Math.floor(skip / limit) + 1}</h2>
        </div>
      </div>

      <div className="sellers-table-container">
        <div className="table-heading">
          <h3>All Sellers</h3>
          <span>{total.toLocaleString('en-IN')} records</span>
        </div>

        {loading ? (
          <div className="sellers-message">Loading sellers...</div>
        ) : error ? (
          <div className="sellers-message error-message">
            {error}
            <button onClick={fetchSellers}>Retry</button>
          </div>
        ) : sellers.length === 0 ? (
          <div className="sellers-message">No sellers found.</div>
        ) : (
          <div className="table-scroll">
            <table className="sellers-table">
              <thead>
                <tr>
                  <th>Seller ID</th>
                  <th>ZIP Code</th>
                  <th>City</th>
                  <th>State</th>
                </tr>
              </thead>

              <tbody>
                {sellers.map((seller) => (
                  <tr key={seller.seller_id}>
                    <td title={seller.seller_id}>
                      {seller.seller_id?.slice(0, 12)}...
                    </td>
                    <td>{seller.seller_zip_code_prefix || '—'}</td>
                    <td>{formatCity(seller.seller_city)}</td>
                    <td>
                      <span className="seller-state">
                        {seller.seller_state || '—'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="sellers-pagination">
          <span>
            Showing {total === 0 ? 0 : skip + 1}–{skip + sellers.length} of{' '}
            {total.toLocaleString('en-IN')}
          </span>

          <div>
            <button
              disabled={skip === 0 || loading}
              onClick={() => setSkip(Math.max(0, skip - limit))}
            >
              Previous
            </button>

            <button
              disabled={skip + limit >= total || loading}
              onClick={() => setSkip(skip + limit)}
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Sellers
