
import { useEffect, useState } from 'react'
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts'
import './Reviews.css'

const API_URL = 'http://127.0.0.1:8000/api/v1'

const COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#06b6d4']

function Reviews() {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchReviews = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch(`${API_URL}/analytics/reviews`)

      if (!response.ok) {
        throw new Error('Unable to fetch review data')
      }

      const data = await response.json()
      setReviews(data)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchReviews()
  }, [])

  const totalReviews = reviews.reduce(
    (sum, item) => sum + item.total_reviews,
    0
  )

  const weightedScore = reviews.reduce(
    (sum, item) => sum + item.review_score * item.total_reviews,
    0
  )

  const averageScore = totalReviews
    ? (weightedScore / totalReviews).toFixed(2)
    : '0.00'

  const positiveReviews = reviews
    .filter((item) => item.review_score >= 4)
    .reduce((sum, item) => sum + item.total_reviews, 0)

  const positivePercentage = totalReviews
    ? ((positiveReviews / totalReviews) * 100).toFixed(1)
    : '0.0'

  if (loading) {
    return <div className="reviews-message">Loading review data...</div>
  }

  if (error) {
    return (
      <div className="reviews-message reviews-error">
        <p>{error}</p>
        <button onClick={fetchReviews}>Try Again</button>
      </div>
    )
  }

  return (
    <div className="reviews-page">
      <div className="reviews-header">
        <div>
          <h2>Customer Reviews</h2>
          <p>Analyze customer feedback and review score distribution.</p>
        </div>

        <button className="reviews-refresh" onClick={fetchReviews}>
          Refresh Data
        </button>
      </div>

      <div className="reviews-kpi-grid">
        <div className="reviews-kpi-card">
          <span>Total Reviews</span>
          <h3>{totalReviews.toLocaleString('en-IN')}</h3>
        </div>

        <div className="reviews-kpi-card">
          <span>Average Review Score</span>
          <h3>{averageScore} / 5</h3>
        </div>

        <div className="reviews-kpi-card">
          <span>Positive Reviews (4–5 Stars)</span>
          <h3>{positivePercentage}%</h3>
          <small>{positiveReviews.toLocaleString('en-IN')} reviews</small>
        </div>
      </div>

      <div className="reviews-chart-card">
        <div className="reviews-section-heading">
          <div>
            <h3>Review Score Distribution</h3>
            <p>Customer reviews grouped by rating from 1 to 5 stars</p>
          </div>
        </div>

        <div className="reviews-chart">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={reviews}
                dataKey="total_reviews"
                nameKey="review_score"
                cx="50%"
                cy="50%"
                outerRadius={115}
                paddingAngle={3}
                label={({ review_score, percent }) =>
                  `${review_score}★ ${(percent * 100).toFixed(1)}%`
                }
              >
                {reviews.map((entry, index) => (
                  <Cell
                    key={entry.review_score}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip />
              <Legend
                formatter={(value) => `${value} Star`}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="reviews-chart-card">
        <div className="reviews-section-heading">
          <div>
            <h3>Rating Details</h3>
            <p>Total customer reviews for each rating</p>
          </div>
        </div>

        <div className="reviews-table-scroll">
          <table className="reviews-table">
            <thead>
              <tr>
                <th>Review Score</th>
                <th>Total Reviews</th>
                <th>Percentage</th>
              </tr>
            </thead>

            <tbody>
              {reviews.map((item) => (
                <tr key={item.review_score}>
                  <td>{item.review_score} ★</td>
                  <td>{item.total_reviews.toLocaleString('en-IN')}</td>
                  <td>
                    {totalReviews
                      ? ((item.total_reviews / totalReviews) * 100).toFixed(2)
                      : '0.00'}
                    %
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="reviews-footer">
        Customer review analytics powered by the Olist e-commerce dataset.
      </div>
    </div>
  )
}

export default Reviews
