import Orders from './components/Orders'
import Customers from './components/Customers'
import Products from './components/Products'
import Sellers from './components/Sellers'
import Analytics from './components/Analytics'
import Payments from './components/Payments'
import Reviews from './components/Reviews'


import { useEffect, useState } from 'react'
import {
  LayoutDashboard, ShoppingCart, Users, Package, Store,
  ChartNoAxesCombined, CreditCard, Star, Search, Bell,
  CalendarDays, ArrowUpRight, ArrowDownRight, Menu,
  ChevronDown, RefreshCw, AlertCircle
} from 'lucide-react'
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
  CartesianGrid, Tooltip, BarChart, Bar, PieChart,
  Pie, Cell
} from 'recharts'
import './App.css'

const API = 'http://127.0.0.1:8000/api/v1'

const navigation = [
  { name: 'Overview', icon: LayoutDashboard },
  { name: 'Orders', icon: ShoppingCart },
  { name: 'Customers', icon: Users },
  { name: 'Products', icon: Package },
  { name: 'Sellers', icon: Store },
  { name: 'Analytics', icon: ChartNoAxesCombined },
  { name: 'Payments', icon: CreditCard },
  { name: 'Reviews', icon: Star },
]

const colors = ['#8b5cf6', '#06b6d4', '#f59e0b', '#ec4899', '#10b981']

function formatNumber(value) {
  return Number(value || 0).toLocaleString('en-IN')
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(Number(value || 0))
}

function formatMonth(value) {
  const [year, month] = value.split('-')
  const date = new Date(Number(year), Number(month) - 1)
  return date.toLocaleDateString('en-IN', {
    month: 'short',
    year: '2-digit'
  })
}

function formatCompactCurrency(value) {
  if (value >= 1000000) return `₹${(value / 1000000).toFixed(1)}M`
  if (value >= 1000) return `₹${(value / 1000).toFixed(0)}K`
  return `₹${value}`
}

function App() {
  const [dashboard, setDashboard] = useState(null)
  const [sales, setSales] = useState([])
  const [statuses, setStatuses] = useState([])
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [active, setActive] = useState('Overview')
  const [mobileOpen, setMobileOpen] = useState(false)
  const [lastUpdated, setLastUpdated] = useState('')

  async function loadDashboard() {
    setLoading(true)
    setError('')

    try {
      const endpoints = [
        `${API}/dashboard/`,
        `${API}/analytics/monthly-sales`,
        `${API}/analytics/order-status`,
        `${API}/analytics/top-products?limit=5`,
        `${API}/analytics/top-categories?limit=5`
      ]

      const responses = await Promise.all(
        endpoints.map(url => fetch(url))
      )

      if (responses.some(response => !response.ok)) {
        throw new Error('Unable to load dashboard data from API.')
      }

      const data = await Promise.all(responses.map(response => response.json()))

      setDashboard(data[0])
      setSales(
  Array.isArray(data[1]?.value)
    ? data[1].value
    : Array.isArray(data[1])
      ? data[1]
      : []
)
// console.log('Monthly Sales Data:', data[1])
      setStatuses(Array.isArray(data[2]) ? data[2] : data[2].data || [])
      setProducts(Array.isArray(data[3]) ? data[3] : data[3].data || [])
      setCategories(Array.isArray(data[4]) ? data[4] : data[4].data || [])
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  const overview = dashboard?.overview || {}
  const customerData = dashboard?.customer_analytics || {}
  const paymentData = dashboard?.payment_distribution || []
  const reviewData = dashboard?.review_analysis || []

  const metrics = [
    {
      title: 'Total Revenue',
      value: formatCurrency(overview.total_revenue),
      icon: CreditCard,
      color: 'purple',
      note: 'Payment value'
    },
    {
      title: 'Total Orders',
      value: formatNumber(overview.total_orders),
      icon: ShoppingCart,
      color: 'cyan',
      note: 'All recorded orders'
    },
    {
      title: 'Total Customers',
      value: formatNumber(overview.total_customers),
      icon: Users,
      color: 'pink',
      note: 'Registered customers'
    },
    {
      title: 'Total Products',
      value: formatNumber(overview.total_products),
      icon: Package,
      color: 'orange',
      note: 'Available products'
    }
  ]

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? 'sidebar-open' : ''}`}>
        <div className="brand">
          <div className="brand-icon"><ChartNoAxesCombined size={25} /></div>
          <div>
            <h2>Olist<span>IQ</span></h2>
            <p>DATA INTELLIGENCE</p>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>
        <nav className="navigation">
          {navigation.map(item => {
            const Icon = item.icon
            return (
              <button
                key={item.name}
                className={`nav-item ${active === item.name ? 'active' : ''}`}
                onClick={() => {
                  setActive(item.name)
                  setMobileOpen(false)
                }}
              >
                <Icon size={19} />
                <span>{item.name}</span>
                {active === item.name && <span className="active-dot" />}
              </button>
            )
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon"><ChartNoAxesCombined size={20} /></div>
            <h3>Data insights</h3>
            <p>Explore your e-commerce performance in one place.</p>
          </div>
          <div className="profile">
            <div className="avatar">AS</div>
            <div className="profile-info">
              <strong>Administrator</strong>
              <span>Project workspace</span>
            </div>
            <ChevronDown size={17} />
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="topbar-left">
            <button className="mobile-menu" onClick={() => setMobileOpen(!mobileOpen)}>
              <Menu size={22} />
            </button>
            <div>
              <div className="breadcrumb">Workspace / <span>{active}</span></div>
              <h1>{active === 'Overview' ? 'Dashboard overview' : active}</h1>
            </div>
          </div>

          
<div className="topbar-actions">
  <div className="live-status"><span /> Live data</div>
  <button className="icon-button" aria-label="Notifications">
    <Bell size={19} />
  </button>
  <div className="top-avatar">AS</div>
</div>
</header>

{active === 'Overview' ? (
  <>
    <section className="welcome-row">

          <div>
            <p className="eyebrow">ECOMMERCE INTELLIGENCE PLATFORM</p>
            <h2>Welcome back <span>👋</span></h2>
            <p className="welcome-subtitle">Here’s what’s happening with your store today.</p>
          </div>
          <div className="date-actions">
            <div className="date-chip"><CalendarDays size={16} /> All time data</div>
            <button className="refresh-button" onClick={loadDashboard} disabled={loading}>
              <RefreshCw size={16} className={loading ? 'spinning' : ''} />
              Refresh
            </button>
          </div>
        </section>

        {error && (
          <div className="error-banner">
            <AlertCircle size={19} />
            <div>
              <strong>Could not load live data</strong>
              <p>{error} Make sure the FastAPI backend is running.</p>
            </div>
            <button onClick={loadDashboard}>Retry</button>
          </div>
        )}

        <section className="metrics-grid">
          {metrics.map((metric, index) => {
            const Icon = metric.icon
            return (
              <article className={`metric-card metric-${metric.color}`} key={metric.title}>
                <div className="metric-top">
                  <div className="metric-icon"><Icon size={21} /></div>
                  <span className="metric-index">0{index + 1}</span>
                </div>
                <p>{metric.title}</p>
                <h3>{loading ? '...' : metric.value}</h3>
                <div className="metric-footer">
                  <span className="metric-note">{metric.note}</span>
                  <ArrowUpRight size={17} />
                </div>
              </article>
            )
          })}
        </section>

        <section className="charts-grid">
          <article className="panel sales-panel">
            <div className="panel-heading">
              <div>
                <span className="panel-kicker">PERFORMANCE</span>
                <h3>Sales overview</h3>
                <p>Monthly revenue trends</p>
              </div>
              <span className="panel-tag">Monthly</span>
            </div>
            <div className="chart-area">
              {sales.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={sales}>
  <defs>
    <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.35} />
      <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
    </linearGradient>
  </defs>

  <CartesianGrid stroke="#293047" strokeDasharray="4 4" vertical={false} />

  {/* <XAxis dataKey="month" stroke="#7d879e" tickLine={false} axisLine={false} /> */}
  <XAxis dataKey="month"tickFormatter={formatMonth}stroke="#7d879e"tickLine={false}axisLine={false}minTickGap={20}/>

  {/* <YAxis stroke="#7d879e" tickLine={false} axisLine={false} /> */}
  <YAxis tickFormatter={formatCompactCurrency}stroke="#7d879e"tickLine={false}axisLine={false}width={65}/>



  {/* <Tooltip contentStyle={{ background: '#151b2d', border: '1px solid #303952', borderRadius: 12 }} /> */}
  {/* <Tooltip labelFormatter={formatMonth}formatter={(value) => [formatCurrency(value), 'Revenue']}contentStyle={{background: '#151b2d',border: '1px solid #303952',borderRadius: 12,color: '#edf0fa',padding: '12px'}}/> */}
  <Tooltip
  labelFormatter={formatMonth}
  formatter={(value) => [formatCurrency(value), 'Revenue']}
  contentStyle={{
    background: '#151b2d',
    border: '1px solid #303952',
    borderRadius: 12,
    color: '#edf0fa',
    padding: '12px'
  }}
/>

  <Area
    type="monotone"
    dataKey="revenue"
    stroke="#9b7bff"
    strokeWidth={3}
    fill="url(#salesGradient)"
    fillOpacity={1}
    dot={false}
    activeDot={{ r: 5 }}
  />
</AreaChart>
                </ResponsiveContainer>
              ) : <div className="empty-chart">{loading ? 'Loading sales data...' : 'Sales data unavailable'}</div>}
            </div>
          </article>

          <article className="panel status-panel">
            <div className="panel-heading">
              <div>
                <span className="panel-kicker">ORDER INSIGHTS</span>
                <h3>Order status</h3>
                <p>Distribution by status</p>
              </div>
            </div>
            <div className="chart-area pie-area">
              {statuses.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={statuses} dataKey="total_orders" nameKey="order_status" innerRadius={65} outerRadius={95} paddingAngle={4}>
                      label={({ percent }) => `${(percent * 100).toFixed(1)}%`}
                      labelLine={false}
                      {statuses.map((entry, index) => <Cell key={entry.order_status || index} fill={colors[index % colors.length]} />)}
                    </Pie>
                    {/* <Tooltip contentStyle={{ background: '#151b2d', border: '1px solid #303952', borderRadius: 12 }} /> */}
                    <Tooltip formatter={(value, name) => [ `${formatNumber(value)} orders`,name]}contentStyle={{background: '#151b2d',border: '1px solid #303952',borderRadius: 12,color: '#edf0fa',padding: '12px'}}/>
                  </PieChart>
                </ResponsiveContainer>
              ) : <div className="empty-chart">{loading ? 'Loading...' : 'Status data unavailable'}</div>}
            </div>
            <div className="status-legend">
              {statuses.slice(0, 4).map((item, index) => (
            <div key={item.order_status || index}>
              <span style={{ background: colors[index] }} />
              {item.order_status}
              <strong>{formatNumber(item.total_orders)}</strong>
            </div>
          ))}
            </div>
          </article>
        </section>

        <section className="lower-grid">
          <article className="panel products-panel">
            <div className="panel-heading">
              <div>
                <span className="panel-kicker">PRODUCT PERFORMANCE</span>
                <h3>Top selling products</h3>
              </div>
              <span className="panel-tag">Top 5</span>
            </div>
            {products.length > 0 ? (
              <div className="table-wrap">
                <table>
                  <thead><tr><th>Product ID</th><th>Category</th><th>Items sold</th><th>Revenue</th></tr></thead>
                  <tbody>
                    {products.map((item, index) => (
                      <tr key={item.product_id || index}>
                        <td><span className="product-symbol">{String(index + 1).padStart(2, '0')}</span>{item.product_id}</td>
                        <td>{item.category || item.product_category_name || 'Uncategorized'}</td>
                        <td>{formatNumber(item.units_sold)}</td>
                        <td className="revenue-cell">{formatCurrency(item.total_sales)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : <div className="empty-table">{loading ? 'Loading products...' : 'Product data unavailable'}</div>}
          </article>

          <article className="panel category-panel">
            <div className="panel-heading">
              <div>
                <span className="panel-kicker">CATEGORY INSIGHTS</span>
                <h3>Top categories</h3>
              </div>
            </div>
            <div className="category-list">
              {categories.length > 0 ? categories.slice(0, 5).map((item, index) => {
                const value = Number(item.units_sold || 0)
                const max = Math.max(...categories.map(c => Number(c.units_sold || 0)), 1)
                return (
                  <div className="category-item" key={item.category || item.product_category_name || index}>
                    <div className="category-info">
                      <span>{item.category || item.product_category_name || 'Other'}</span>
                      <strong>{formatNumber(value)}</strong>
                    </div>
                    <div className="progress-track"><div style={{ width: `${value / max * 100}%`, background: colors[index] }} /></div>
                  </div>
                )
              }) : <div className="empty-table">{loading ? 'Loading...' : 'Category data unavailable'}</div>}
            </div>
          </article>
        </section>

        <footer className="footer">
  <span>© 2026 OlistIQ · E-Commerce Data Intelligence</span>
  <span>{lastUpdated ? `Last updated ${lastUpdated}` : 'Connecting to backend...'}</span>
</footer>
  </>
) : active === 'Orders' ? (
  <Orders />
) : active === 'Customers' ? (
  <Customers />
) : active === 'Products' ? (
  <Products />
) : active === 'Sellers' ? (
  <Sellers />
) : active === 'Analytics' ? (
  <Analytics />
) : active === 'Payments' ? (
  <Payments />
) : active === 'Reviews' ? (
  <Reviews />
) : (
  <div className="empty-chart">
    {active} page is coming soon.
  </div>
)}
      </main>
    </div>
  )
}

export default App
