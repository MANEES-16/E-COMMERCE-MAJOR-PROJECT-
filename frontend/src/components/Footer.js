// src/components/Footer.js
import { Container, Row, Col } from 'react-bootstrap'

const Footer = () => {
  return (
    <footer>
      <Container>
        <Row>
          <Col className='text-center py-3'>
            &copy; {new Date().getFullYear()} Ecommerce
          </Col>
        </Row>
      </Container>
    </footer>
  )
}

export default Footer