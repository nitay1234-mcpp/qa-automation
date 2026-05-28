import React from 'react';
import renderer from 'react-test-renderer';

// Example PaymentFlow component stub
const PaymentFlow = ({ amount, currency, status }) => {
  return (
    <div>
      <h1>Payment Flow</h1>
      <p>Amount: {amount} {currency}</p>
      <p>Status: {status}</p>
    </div>
  );
};

// Snapshot test
describe('PaymentFlow UI', () => {
  it('renders correctly with success status', () => {
    const tree = renderer.create(
      <PaymentFlow amount={100} currency="USD" status="success" />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('renders correctly with pending status', () => {
    const tree = renderer.create(
      <PaymentFlow amount={100} currency="USD" status="pending" />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('renders correctly with failure status', () => {
    const tree = renderer.create(
      <PaymentFlow amount={100} currency="USD" status="failed" />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
