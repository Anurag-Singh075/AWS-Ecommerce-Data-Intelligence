import './Orders.css'
import { useEffect, useState } from 'react'

const API_URL = 'http://127.0.0.1:8000/api/v1'

function Orders() {
  const [orders, setOrders] = useState([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const limit = 20

  const fetchOrders = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch(
        `${API_URL}/orders/?skip=${skip}&limit=${limit}`
      )

      if (!response.ok) {
        throw new Error('Failed to fetch orders')
      }

      const data = await response.json()

      setOrders(data.orders || [])
      setTotal(data.total || 0)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchOrders()
  }, [skip])

  const formatDate = (date) => {
    if (!date) return '—'

    return new Date(date).toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    })
  }

  const formatStatus = (status) => {
    return status
      ? status.replaceAll('_', ' ').replace(/\b\w/g, char => char.toUpperCase())
      : 'Unknown'
  }

  const getStatusClass = (status) => {
    const classes = {
      delivered: 'status-delivered',
      shipped: 'status-shipped',
      canceled: 'status-canceled',
      unavailable: 'status-canceled',
      processing: 'status-processing',
      invoiced: 'status-processing',
      approved: 'status-processing',
      created: 'status-processing'
    }

    return classes[status] || 'status-default'
  }

  return (
    <div className="orders-page">

      <div className="page-header">
        <div>
          <h2>Orders</h2>
          <p>Manage and monitor all e-commerce orders.</p>
        </div>

        <button className="refresh-btn" onClick={fetchOrders}>
          ↻ Refresh
        </button>
      </div>

      <div className="orders-summary">
        <div className="orders-summary-card">
          <span>Total Orders</span>
          <h2>{total.toLocaleString('en-IN')}</h2>
        </div>

        <div className="orders-summary-card">
          <span>Showing Orders</span>
          <h2>{orders.length}</h2>
        </div>

        <div className="orders-summary-card">
          <span>Current Page</span>
          <h2>{Math.floor(skip / limit) + 1}</h2>
        </div>
      </div>

      <div className="orders-table-container">

        <div className="table-heading">
          <h3>All Orders</h3>
          <span>{total.toLocaleString('en-IN')} records</span>
        </div>

        {loading ? (
          <div className="orders-message">Loading orders...</div>
        ) : error ? (
          <div className="orders-message error-message">
            {error}
            <button onClick={fetchOrders}>Retry</button>
          </div>
        ) : orders.length === 0 ? (
          <div className="orders-message">No orders found.</div>
        ) : (
          <div className="table-scroll">
            <table className="orders-table">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Customer ID</th>
                  <th>Status</th>
                  <th>Purchase Date</th>
                  <th>Estimated Delivery</th>
                </tr>
              </thead>

              <tbody>
                {orders.map((order) => (
                  <tr key={order.order_id}>
                    <td title={order.order_id}>
                      {order.order_id?.slice(0, 12)}...
                    </td>

                    <td title={order.customer_id}>
                      {order.customer_id?.slice(0, 12)}...
                    </td>

                    <td>
                      <span className={`order-status ${getStatusClass(order.order_status)}`}>
                        {formatStatus(order.order_status)}
                      </span>
                    </td>

                    <td>
                      {formatDate(order.order_purchase_timestamp)}
                    </td>

                    <td>
                      {formatDate(order.order_estimated_delivery_date)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="orders-pagination">
          <span>
            Showing {total === 0 ? 0 : skip + 1}–{skip + orders.length} of {total.toLocaleString('en-IN')}
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

export default Orders
