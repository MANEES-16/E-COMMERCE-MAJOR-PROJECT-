// src/components/Product.js
import { Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'

const Product = ({ product }) => {
  const imageSrc = product.image && !product.image.startsWith('http')
    ? `${process.env.PUBLIC_URL}${product.image}`
    : product.image
  const fallbackImage = 'https://via.placeholder.com/300x300?text=No+Image'

  return (
    <Card className='my-3 p-3 rounded'>
      <Link to={`/product/${product._id}`}>
        <Card.Img src={imageSrc || fallbackImage} variant='top' />
      </Link>

      <Card.Body>
        <Link to={`/product/${product._id}`}>
          <Card.Title as='div'>
            <strong>{product.name}</strong>
          </Card.Title>
        </Link>

        <Card.Text as='h3'>${product.price}</Card.Text>
      </Card.Body>
    </Card>
  )
}

export default Product