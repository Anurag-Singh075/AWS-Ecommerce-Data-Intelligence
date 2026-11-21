
import { useEffect, useState } from 'react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts'
import './Analytics.css'

const API_URL = 'http://127.0.0.1:8000/api/v1'

const COLORS = [
  '#8b5cf6',
  '#06b6d4',
  '#f59e0b',
  '#ec4899',
  '#10b981',
  '#3b82f6',
  '#f97316',
  '#a855f7'
]

const formatCurrency = (value) =>
  `₹${Number(value || 0).toLocaleString('en-IN', {
    maximumFractionDigits: 0
  })}`

const formatNumber = (value) =>
  Number(value || 0).toLocaleString('en-IN')

const formatLabel = (value) =>
  String(value || '')
    .replaceAll('_', ' ')
    .replace(/\b\w/g, char => char.toUpperCase())

function Analytics() {
  const [data, setData] = useState({
    overview: null,
    monthlySales: [],
    orderStatus: [],
    topProducts: [],
    topCategories: [],
    customers: null,
    sellerPerformance: [],
    payments: [],
    reviews: []
  })

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      setError('')

      const endpoints = [
        'analytics/overview',
        'analytics/monthly-sales',
        'analytics/order-status',
        'analytics/top-products',
        'analytics/top-categories',
        'analytics/customers',
        'analytics/seller-performance',
        'analytics/payments',
        'analytics/reviews'
      ]

      const responses = await Promise.all(
        endpoints.map(endpoint =>
          fetch(`${API_URL}/${endpoint}`)
        )
      )

      const failedResponse = responses.find(response => !response.ok)

      if (failedResponse) {
        throw new Error('Failed to load analytics data from backend.')
      }

      const results = await Promise.all(
        responses.map(response => response.json())
      )

      setData({
        overview: results[0],
        monthlySales: results[1],
        orderStatus: results[2],
        topProducts: results[3],
        topCategories: results[4],
        customers: results[5],
        sellerPerformance: results[6],
        payments: results[7],
        reviews: results[8]
      })
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAnalytics()
  }, [])

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="analytics-message">
          Loading analytics data...
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analytics-page">
        <div className="analytics-message analytics-error">
          <p>{error}</p>
          <button onClick={fetchAnalytics}>Retry</button>
        </div>
      </div>
    )
  }

  const overview = data.overview || {}
  const customers = data.customers || {}

  const monthlyData = data.monthlySales.map(item => ({
    ...item,
    month: item.month
  }))

  const paymentData = data.payments.filter(
    item => item.payment_type !== 'not_defined'
  )

  const reviewData = data.reviews.map(item => ({
    ...item,
    rating: `${item.review_score} Star`
  }))

  const orderStatusData = data.orderStatus.map(item => ({
    ...item,
    name: formatLabel(item.order_status)
  }))

  const customerData = [
    {
      name: 'One-Time Customers',
      value: customers.one_time_customers || 0
    },
    {
      name: 'Repeat Customers',
      value: customers.repeat_customers || 0
    }
  ]

  const paymentChartData = paymentData.map(item => ({
    ...item,
    name: formatLabel(item.payment_type)
  }))

  return (
    <div className="analytics-page">

      <div className="analytics-header">
        <div>
          <h2>Business Analytics</h2>
          <p>
            Complete insights into your e-commerce business performance.
          </p>
        </div>

        <button
          className="analytics-refresh"
          onClick={fetchAnalytics}
        >
          ↻ Refresh Data
        </button>
      </div>

      {/* Overview KPI Cards */}

      <section className="analytics-kpi-grid">

        <div className="analytics-kpi-card">
          <span>Total Revenue</span>
          <h3>{formatCurrency(overview.total_revenue)}</h3>
        </div>

        <div className="analytics-kpi-card">
          <span>Total Orders</span>
          <h3>{formatNumber(overview.total_orders)}</h3>
        </div>

        <div className="analytics-kpi-card">
          <span>Total Customers</span>
          <h3>{formatNumber(overview.total_customers)}</h3>
        </div>

        <div className="analytics-kpi-card">
          <span>Total Products</span>
          <h3>{formatNumber(overview.total_products)}</h3>
        </div>

        <div className="analytics-kpi-card">
          <span>Total Sellers</span>
          <h3>{formatNumber(overview.total_sellers)}</h3>
        </div>

        <div className="analytics-kpi-card">
          <span>Order Items</span>
          <h3>{formatNumber(overview.total_order_items)}</h3>
        </div>

      </section>

      {/* Monthly Revenue Chart */}

      <section className="analytics-chart-card">
        <div className="analytics-section-heading">
          <div>
            <h3>Monthly Revenue Trend</h3>
            <p>Revenue generated across different months</p>
          </div>
        </div>

        <div className="analytics-chart">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={monthlyData}>
              <defs>
                <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                </linearGradient>
              </defs>

              <CartesianGrid stroke="#303952" strokeDasharray="3 3" />
              <XAxis dataKey="month" stroke="#929bb3" />
              <YAxis
                stroke="#929bb3"
                tickFormatter={value => `₹${(value / 100000).toFixed(0)}L`}
              />

              <Tooltip
                formatter={value => [formatCurrency(value), 'Revenue']}
                contentStyle={{
                  background: '#151b2d',
                  border: '1px solid #303952',
                  borderRadius: 12,
                  color: '#edf0fa'
                }}
              />

              <Area
                type="monotone"
                dataKey="revenue"
                stroke="#8b5cf6"
                strokeWidth={3}
                fill="url(#revenueGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Monthly Orders and Order Status */}

      <section className="analytics-two-column">

        <div className="analytics-chart-card">
          <div className="analytics-section-heading">
            <div>
              <h3>Monthly Orders</h3>
              <p>Number of orders per month</p>
            </div>
          </div>

          <div className="analytics-chart">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyData}>
                <CartesianGrid stroke="#303952" strokeDasharray="3 3" />
                <XAxis dataKey="month" stroke="#929bb3" />
                <YAxis stroke="#929bb3" />

                <Tooltip
                  formatter={value => [formatNumber(value), 'Orders']}
                  contentStyle={{
                    background: '#151b2d',
                    border: '1px solid #303952',
                    borderRadius: 12
                  }}
                />

                <Bar
                  dataKey="total_orders"
                  fill="#06b6d4"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="analytics-chart-card">
          <div className="analytics-section-heading">
            <div>
              <h3>Order Status Distribution</h3>
              <p>Orders grouped by current status</p>
            </div>
          </div>

          <div className="analytics-chart">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={orderStatusData}
                  dataKey="total_orders"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={105}
                  paddingAngle={3}
                >
                  {orderStatusData.map((entry, index) => (
                    <Cell
                      key={entry.order_status}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>

                <Tooltip
                  formatter={value => formatNumber(value)}
                  contentStyle={{
                    background: '#151b2d',
                    border: '1px solid #303952',
                    borderRadius: 12
                  }}
                />

                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </section>

      {/* Top Products */}

      <section className="analytics-chart-card">
        <div className="analytics-section-heading">
          <div>
            <h3>Top Selling Products</h3>
            <p>Top 10 products based on units sold</p>
          </div>
        </div>

        <div className="analytics-chart">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.topProducts} layout="vertical">
              <CartesianGrid stroke="#303952" strokeDasharray="3 3" />

              <XAxis type="number" stroke="#929bb3" />
              <YAxis
                type="category"
                dataKey="product_id"
                width={100}
                stroke="#929bb3"
                tickFormatter={value => value.slice(0, 8)}
              />

              <Tooltip
                formatter={value => [formatNumber(value), 'Units Sold']}
                contentStyle={{
                  background: '#151b2d',
                  border: '1px solid #303952',
                  borderRadius: 12
                }}
              />

              <Bar
                dataKey="units_sold"
                fill="#8b5cf6"
                radius={[0, 5, 5, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Top Categories */}

      <section className="analytics-chart-card">
        <div className="analytics-section-heading">
          <div>
            <h3>Top Product Categories</h3>
            <p>Category-wise sales performance</p>
          </div>
        </div>

        <div className="analytics-chart">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.topCategories}>
              <CartesianGrid stroke="#303952" strokeDasharray="3 3" />

              <XAxis
                dataKey="category"
                stroke="#929bb3"
                tickFormatter={formatLabel}
              />

              <YAxis
                stroke="#929bb3"
                tickFormatter={value => `₹${(value / 1000).toFixed(0)}K`}
              />

              <Tooltip
                labelFormatter={formatLabel}
                formatter={value => [formatCurrency(value), 'Sales']}
                contentStyle={{
                  background: '#151b2d',
                  border: '1px solid #303952',
                  borderRadius: 12
                }}
              />

              <Bar
                dataKey="total_sales"
                fill="#10b981"
                radius={[5, 5, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Customer Analytics */}

      <section className="analytics-two-column">

        <div className="analytics-chart-card">
          <div className="analytics-section-heading">
            <div>
              <h3>Customer Analytics</h3>
              <p>Repeat vs one-time customers</p>
            </div>
          </div>

          <div className="analytics-chart">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={customerData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={105}
                  paddingAngle={4}
                >
                  <Cell fill="#06b6d4" />
                  <Cell fill="#8b5cf6" />
                </Pie>

                <Tooltip
                  formatter={value => formatNumber(value)}
                  contentStyle={{
                    background: '#151b2d',
                    border: '1px solid #303952',
                    borderRadius: 12
                  }}
                />

                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="customer-stat-row">
            <span>Unique Customers</span>
            <strong>{formatNumber(customers.total_unique_customers)}</strong>
          </div>
        </div>

        {/* Payment Analytics */}

        <div className="analytics-chart-card">
          <div className="analytics-section-heading">
            <div>
              <h3>Payment Analytics</h3>
              <p>Revenue by payment method</p>
            </div>
          </div>

          <div className="analytics-chart">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={paymentChartData}
                  dataKey="total_amount"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={105}
                  paddingAngle={4}
                >
                  {paymentChartData.map((entry, index) => (
                    <Cell
                      key={entry.payment_type}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>

                <Tooltip
                  formatter={value => formatCurrency(value)}
                  contentStyle={{
                    background: '#151b2d',
                    border: '1px solid #303952',
                    borderRadius: 12
                  }}
                />

                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </section>

      {/* Seller Performance */}

      <section className="analytics-chart-card">
        <div className="analytics-section-heading">
          <div>
            <h3>Top Seller Performance</h3>
            <p>Top 10 sellers ranked by total sales</p>
          </div>
        </div>

        <div className="analytics-table-scroll">
          <table className="analytics-table">
            <thead>
              <tr>
                <th>Seller ID</th>
                <th>Location</th>
                <th>Items Sold</th>
                <th>Orders</th>
                <th>Total Sales</th>
              </tr>
            </thead>

            <tbody>
              {data.sellerPerformance.map(seller => (
                <tr key={seller.seller_id}>
                  <td title={seller.seller_id}>
                    {seller.seller_id.slice(0, 12)}...
                  </td>
                  <td>
                    {formatLabel(seller.city)}, {seller.state}
                  </td>
                  <td>{formatNumber(seller.total_items_sold)}</td>
                  <td>{formatNumber(seller.total_orders)}</td>
                  <td>{formatCurrency(seller.total_sales)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Review Analytics */}

      <section className="analytics-chart-card">
        <div className="analytics-section-heading">
          <div>
            <h3>Customer Review Analytics</h3>
            <p>Distribution of customer ratings</p>
          </div>
        </div>

        <div className="analytics-chart">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={reviewData}>
              <CartesianGrid stroke="#303952" strokeDasharray="3 3" />
              <XAxis dataKey="rating" stroke="#929bb3" />
              <YAxis stroke="#929bb3" />

              <Tooltip
                formatter={value => [formatNumber(value), 'Reviews']}
                contentStyle={{
                  background: '#151b2d',
                  border: '1px solid #303952',
                  borderRadius: 12
                }}
              />

              <Bar
                dataKey="total_reviews"
                fill="#f59e0b"
                radius={[5, 5, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <div className="analytics-footer">
        Analytics data is powered by your local FastAPI backend.
      </div>

    </div>
  )
}

export default Analytics
