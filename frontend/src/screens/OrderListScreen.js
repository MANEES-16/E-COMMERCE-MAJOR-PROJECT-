// src/screens/OrderListScreen.js
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Table, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import Message from '../components/Message'
import Loader from '../components/Loader'
import { listOrders } from '../actions/orderActions'

const OrderListScreen = () => {
  const dispatch = useDispatch()

  const orderList = useSelector((state) => state.orderList)
  const { loading, error, orders } = orderList

  const { userInfo } = useSelector((state) => state.userLogin)

  useEffect(() => {
    if (userInfo && userInfo.isAdmin) {
      dispatch(listOrders())
    }
  }, [dispatch, userInfo])

  return (
    <>
      <h1>Orders</h1>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error}</Message>
      ) : (
        <Table striped bordered hover responsive className='table-sm'>
          <thead>
            <tr>
              <th>ID</th>
              <th>USER</th>
              <th>DATE</th>
              <th>TOTAL</th>
              <th>PAID</th>
              <th>DELIVERED</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {orders &&
              orders.map((order) => (
                <tr key={order._id}>
                  <td>{order._id}</td>
                  <td>{order.user && order.user.name}</td>
                  <td>{order.createdAt.substring(0, 10)}</td>
                  <td>{order.totalPrice}</td>
                  <td>{order.isPaid ? 'Yes' : 'No'}</td>
                  <td>{order.isDelivered ? 'Yes' : 'No'}</td>
                  <td>
                    <Link to={`/order/${order._id}`}>
                      <Button variant='light' className='btn-sm'>
                        Details
                      </Button>
                    </Link>
                  </td>
                </tr>
              ))}
          </tbody>
        </Table>
      )}
    </>
  )
}

export default OrderListScreen