
import { useEffect, useState } from 'react'
import './Customers.css'

const API_URL = 'http://127.0.0.1:8000/api/v1'

function Customers() {
  const [customers, setCustomers] = useState([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const limit = 20

  const fetchCustomers = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch(
        `${API_URL}/customers/?skip=${skip}&limit=${limit}`
      )

      if (!response.ok) {
        throw new Error('Failed to fetch customers')
      }

      const data = await response.json()

      setCustomers(data.customers || [])
      setTotal(data.total || 0)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCustomers()
  }, [skip])

  return (
    <div className="customers-page">

      <div className="page-header">
        <div>
          <h2>Customers</h2>
          <p>Explore customer records and geographical distribution.</p>
        </div>

        <button className="refresh-btn" onClick={fetchCustomers}>
          ↻ Refresh
        </button>
      </div>

      <div className="customers-summary">
        <div className="customers-summary-card">
          <span>Total Customers</span>
          <h2>{total.toLocaleString('en-IN')}</h2>
        </div>

        <div className="customers-summary-card">
          <span>Showing Customers</span>
          <h2>{customers.length}</h2>
        </div>

        <div className="customers-summary-card">
          <span>Current Page</span>
          <h2>{Math.floor(skip / limit) + 1}</h2>
        </div>
      </div>

      <div className="customers-table-container">

        <div className="table-heading">
          <h3>All Customers</h3>
          <span>{total.toLocaleString('en-IN')} records</span>
        </div>

        {loading ? (
          <div className="customers-message">Loading customers...</div>
        ) : error ? (
          <div className="customers-message error-message">
            {error}
            <button onClick={fetchCustomers}>Retry</button>
          </div>
        ) : customers.length === 0 ? (
          <div className="customers-message">No customers found.</div>
        ) : (
          <div className="table-scroll">
            <table className="customers-table">
              <thead>
                <tr>
                  <th>Customer ID</th>
                  <th>Unique Customer ID</th>
                  <th>ZIP Code</th>
                  <th>City</th>
                  <th>State</th>
                </tr>
              </thead>

              <tbody>
                {customers.map((customer) => (
                  <tr key={customer.customer_id}>
                    <td title={customer.customer_id}>
                      {customer.customer_id?.slice(0, 12)}...
                    </td>

                    <td title={customer.customer_unique_id}>
                      {customer.customer_unique_id?.slice(0, 12)}...
                    </td>

                    <td>{customer.customer_zip_code_prefix}</td>

                    <td className="city-name">
                      {customer.customer_city}
                    </td>

                    <td>
                      <span className="customer-state">
                        {customer.customer_state}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="customers-pagination">
          <span>
            Showing {total === 0 ? 0 : skip + 1}–{skip + customers.length} of {total.toLocaleString('en-IN')}
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

export default Customers
