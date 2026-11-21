
import { useEffect, useState } from 'react'
import './Products.css'

const API_URL = 'http://127.0.0.1:8000/api/v1'

function Products() {
  const [products, setProducts] = useState([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const limit = 20

  const fetchProducts = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch(
        `${API_URL}/products/?skip=${skip}&limit=${limit}`
      )

      if (!response.ok) {
        throw new Error('Failed to fetch products')
      }

      const data = await response.json()

      setProducts(data.products || [])
      setTotal(data.total || 0)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [skip])

  const formatCategory = (category) => {
    return category
      ? category.replaceAll('_', ' ').replace(/\b\w/g, char => char.toUpperCase())
      : 'Uncategorized'
  }

  const formatWeight = (weight) => {
    return weight ? `${(Number(weight) / 1000).toFixed(2)} kg` : '—'
  }

  const formatDimensions = (product) => {
    return `${product.product_length_cm || 0} × ${product.product_height_cm || 0} × ${product.product_width_cm || 0} cm`
  }

  return (
    <div className="products-page">

      <div className="page-header">
        <div>
          <h2>Products</h2>
          <p>Explore product catalog and physical specifications.</p>
        </div>

        <button className="refresh-btn" onClick={fetchProducts}>
          ↻ Refresh
        </button>
      </div>

      <div className="products-summary">
        <div className="products-summary-card">
          <span>Total Products</span>
          <h2>{total.toLocaleString('en-IN')}</h2>
        </div>

        <div className="products-summary-card">
          <span>Showing Products</span>
          <h2>{products.length}</h2>
        </div>

        <div className="products-summary-card">
          <span>Current Page</span>
          <h2>{Math.floor(skip / limit) + 1}</h2>
        </div>
      </div>

      <div className="products-table-container">

        <div className="table-heading">
          <h3>All Products</h3>
          <span>{total.toLocaleString('en-IN')} records</span>
        </div>

        {loading ? (
          <div className="products-message">Loading products...</div>
        ) : error ? (
          <div className="products-message error-message">
            {error}
            <button onClick={fetchProducts}>Retry</button>
          </div>
        ) : products.length === 0 ? (
          <div className="products-message">No products found.</div>
        ) : (
          <div className="table-scroll">
            <table className="products-table">
              <thead>
                <tr>
                  <th>Product ID</th>
                  <th>Category</th>
                  <th>Photos</th>
                  <th>Weight</th>
                  <th>Dimensions (L × H × W)</th>
                </tr>
              </thead>

              <tbody>
                {products.map((product) => (
                  <tr key={product.product_id}>
                    <td title={product.product_id}>
                      {product.product_id?.slice(0, 12)}...
                    </td>

                    <td>
                      <span className="product-category">
                        {formatCategory(product.product_category_name)}
                      </span>
                    </td>

                    <td>{product.product_photos_qty ?? '—'}</td>

                    <td>{formatWeight(product.product_weight_g)}</td>

                    <td>{formatDimensions(product)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="products-pagination">
          <span>
            Showing {total === 0 ? 0 : skip + 1}–{skip + products.length} of {total.toLocaleString('en-IN')}
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

export default Products
