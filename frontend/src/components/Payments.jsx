
import { useEffect, useState } from 'react'
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts'
import './Payments.css'

const API_URL = 'http://127.0.0.1:8000/api/v1'

const COLORS = ['#6366f1', '#22c55e', '#f59e0b', '#ec4899', '#06b6d4']

function Payments() {
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchPayments = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch(`${API_URL}/analytics/payments`)

      if (!response.ok) {
        throw new Error('Unable to fetch payment data')
      }

      const data = await response.json()
      setPayments(data)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPayments()
  }, [])

  const totalTransactions = payments.reduce(
    (sum, item) => sum + item.total_transactions,
    0
  )

  const totalAmount = payments.reduce(
    (sum, item) => sum + item.total_amount,
    0
  )

  const formatCurrency = (value) =>
    `₹${Number(value).toLocaleString('en-IN', {
      maximumFractionDigits: 2
    })}`

  if (loading) {
    return <div className="payments-message">Loading payment data...</div>
  }

  if (error) {
    return (
      <div className="payments-message payments-error">
        <p>{error}</p>
        <button onClick={fetchPayments}>Try Again</button>
      </div>
    )
  }

  return (
    <div className="payments-page">
      <div className="payments-header">
        <div>
          <h2>Payment Analytics</h2>
          <p>Understand payment methods and transaction distribution.</p>
        </div>

        <button className="payments-refresh" onClick={fetchPayments}>
          Refresh Data
        </button>
      </div>

      <div className="payments-kpi-grid">
        <div className="payments-kpi-card">
          <span>Total Transactions</span>
          <h3>{totalTransactions.toLocaleString('en-IN')}</h3>
        </div>

        <div className="payments-kpi-card">
          <span>Total Payment Amount</span>
          <h3>{formatCurrency(totalAmount)}</h3>
        </div>

        <div className="payments-kpi-card">
          <span>Payment Methods</span>
          <h3>{payments.length}</h3>
        </div>
      </div>

      <div className="payments-chart-card">
        <div className="payments-section-heading">
          <div>
            <h3>Payment Method Distribution</h3>
            <p>Transaction count by payment type</p>
          </div>
        </div>

        <div className="payments-chart">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={payments}
                dataKey="total_transactions"
                nameKey="payment_type"
                cx="50%"
                cy="50%"
                outerRadius={110}
                paddingAngle={3}
                label
              >
                {payments.map((entry, index) => (
                  <Cell
                    key={entry.payment_type}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="payments-chart-card">
        <div className="payments-section-heading">
          <div>
            <h3>Payment Method Details</h3>
            <p>Transaction count and amount for each payment method</p>
          </div>
        </div>

        <div className="payments-table-scroll">
          <table className="payments-table">
            <thead>
              <tr>
                <th>Payment Type</th>
                <th>Total Transactions</th>
                <th>Total Amount</th>
              </tr>
            </thead>

            <tbody>
              {payments.map((payment) => (
                <tr key={payment.payment_type}>
                  <td>{payment.payment_type.replaceAll('_', ' ')}</td>
                  <td>
                    {payment.total_transactions.toLocaleString('en-IN')}
                  </td>
                  <td>{formatCurrency(payment.total_amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="payments-footer">
        Payment analytics powered by the Olist e-commerce dataset.
      </div>
    </div>
  )
}

export default Payments
