
describe("PathIterator", function() {
  beforeEach(function() {
    testPoints = [
      {lat: 20, lng: 20, time: Date.UTC(2012, 1, 1, 1, 1, 1)},
      {lat: 20, lng: 20, time: Date.UTC(2012, 1, 1, 1, 4, 1)},
      {lat: 20, lng: 20, time: Date.UTC(2012, 1, 1, 6, 4, 1)},
      {lat: 20, lng: 20, time: Date.UTC(2012, 1, 3, 6, 4, 1)},
      {lat: 20, lng: 20, time: Date.UTC(2012, 7, 3, 6, 4, 1)},
      {lat: 20, lng: 20, time: Date.UTC(2014, 7, 3, 6, 4, 1)}
    ];
    pathIterator = new PathIterator(testPoints);
  });

  it("returns the last passed point", function() {
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 1, 1, 1, 1, 2))).toEqual(testPoints[0]);
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 1, 1, 1, 3, 1))).toEqual(testPoints[0]);
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 1, 1, 6, 3, 1))).toEqual(testPoints[1]);
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 7, 3, 6, 5, 1))).toEqual(testPoints[4]);
    expect(pathIterator.getPointAtTime(Date.UTC(2013, 1, 1, 6, 3, 1))).toEqual(testPoints[4]);
  });

  it("returns the current point if exactly on the point", function() {
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 1, 1, 1, 1, 1))).toEqual(testPoints[0]);
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 1, 1, 1, 4, 1))).toEqual(testPoints[1]);
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 1, 1, 6, 4, 1))).toEqual(testPoints[2]);
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 7, 3, 6, 4, 1))).toEqual(testPoints[4]);
    expect(pathIterator.getPointAtTime(Date.UTC(2014, 7, 3, 6, 4, 1))).toEqual(testPoints[5]);
  });

  it("does not return a point if the selected time is before any point", function() {
    expect(pathIterator.getPointAtTime(Date.UTC(2012, 1, 1, 1, 1, 0))).toBe(null);
  });

  it("returns the last point if the selected time is after all points", function() {
    expect(pathIterator.getPointAtTime(Date.UTC(2014, 7, 3, 6, 4, 2))).toEqual(testPoints[5]);
  })


});